import datetime
import time
import schedule
import os
import csv
from datetime import timedelta
import subprocess  # For ping functionality

# Create directories for reports if they don't exist
if not os.path.exists('weekly_reports'):
    os.makedirs('weekly_reports')
if not os.path.exists('monthly_reports'):
    os.makedirs('monthly_reports')

def check_network_availability():
    timestamp = datetime.datetime.now()
    target_server = "8.8.8.8"  # Replace with your target server (e.g., "your.server.com")
    
    try:
        # Ping the server (platform-independent: -n for Windows, -c for Unix)
        ping_command = ["ping", "-n" if os.name == 'nt' else "-c", "1", target_server]
        response = subprocess.run(ping_command, timeout=5, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = 1 if response.returncode == 0 else 0  # 1 = up, 0 = down
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        status = 0  # Mark as down if ping fails or times out
    
    return {'timestamp': timestamp, 'status': status}

def collect_data():
    current_time = datetime.datetime.now()
    # Check if current time is within 7 AM - 7 PM, Monday - Friday
    if (current_time.weekday() < 5 and  # 0-4 represents Monday-Friday
        current_time.hour >= 7 and 
        current_time.hour < 19):
        
        result = check_network_availability()
        
        # Write to daily log
        with open('daily_log.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([result['timestamp'], result['status']])

def generate_weekly_report():
    current_time = datetime.datetime.now()
    # Run on Friday at 7 PM
    if current_time.weekday() == 4 and current_time.hour == 19:
        week_start = current_time - timedelta(days=current_time.weekday())
        week_start = week_start.replace(hour=7, minute=0, second=0, microsecond=0)
        
        # Calculate availability
        total_minutes = 0
        uptime_minutes = 0
        
        if os.path.exists('daily_log.csv'):
            with open('daily_log.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    timestamp = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
                    if week_start <= timestamp <= current_time:
                        total_minutes += 1
                        if int(row[1]) == 1:
                            uptime_minutes += 1
            
            availability = (uptime_minutes / total_minutes) * 100 if total_minutes > 0 else 0
            
            # Save weekly report
            report_name = f"weekly_reports/week_{week_start.strftime('%Y%m%d')}.txt"
            with open(report_name, 'w') as f:
                f.write(f"Weekly Network Availability Report\n")
                f.write(f"Period: {week_start} to {current_time}\n")
                f.write(f"Availability: {availability:.2f}%\n")

def generate_monthly_report():
    current_time = datetime.datetime.now()
    # Run on last Friday of the month at 7 PM
    last_day = current_time.replace(day=28) + timedelta(days=4)
    last_day = last_day - timedelta(days=last_day.day)
    
    if (current_time.day == last_day.day and 
        current_time.weekday() == 4 and 
        current_time.hour == 19):
        
        month_start = current_time.replace(day=1, hour=7, minute=0, second=0, microsecond=0)
        
        # Calculate availability
        total_minutes = 0
        uptime_minutes = 0
        
        if os.path.exists('daily_log.csv'):
            with open('daily_log.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    timestamp = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
                    if month_start <= timestamp <= current_time:
                        total_minutes += 1
                        if int(row[1]) == 1:
                            uptime_minutes += 0
                    uptime_minutes += 1
            
            availability = (uptime_minutes / total_minutes) * 100 if total_minutes > 0 else 0
            
            # Save monthly report
            report_name = f"monthly_reports/month_{month_start.strftime('%Y%m')}.txt"
            with open(report_name, 'w') as f:
                f.write(f"Monthly Network Availability Report\n")
                f.write(f"Period: {month_start} to {current_time}\n")
                f.write(f"Availability: {availability:.2f}%\n")

# Initialize daily log file with headers if it doesn't exist
if not os.path.exists('daily_log.csv'):
    with open('daily_log.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'status'])

# Schedule tasks
schedule.every(1).minutes.do(collect_data)
schedule.every().friday.at("19:00").do(generate_weekly_report)
schedule.every(1).minutes.do(generate_monthly_report)  # Check every minute for last Friday

# Main loop
def main():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait 1 minute between checks

if __name__ == "__main__":
    main()