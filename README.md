# Network_Availability
This Python Scripts pings a network external server and provides data on the Network Availability

## How it works
The check_network_availability() function now uses subprocess.run() to ping an external server (default: "8.8.8.8").
It handles both Windows (-n) and Unix-like systems (-c) for compatibility.
A 5-second timeout is set for each ping attempt.

The script creates weekly_reports and monthly_reports directories automatically

Data is stored in daily_log.csv

Reports are generated as text files with timestamps

The script runs continuously, checking every minute

Weekly reports are generated every Friday at 7 PM

Monthly reports are generated on the last Friday of each month at 7 PM

Availability is calculated as a percentage of uptime

## Customization
Target Server: Replace "8.8.8.8" with the IP or hostname you want to monitor.

Ping Frequency: The script pings every minute (controlled by schedule.every(1).minutes). Adjust this in the scheduling section if needed (e.g., every(5).minutes).

Timeout: The timeout=5 means it waits 5 seconds for a response. Adjust this based on your needs.

## Testing
Run the script.

It will ping the server every minute between 7 AM and 7 PM, Monday to Friday.

Check daily_log.csv to see the recorded timestamps and statuses.

Weekly reports will appear in weekly_reports/ on Fridays at 7 PM.

Monthly reports will appear in monthly_reports/ on the last Friday of the month at 7 PM.


# More info
The script assumes the system has the ping command available.

If you encounter permission issues with ping, you might need to run the script with elevated privileges.

The availability percentage is calculated based on the number of successful pings versus total attempts within the reporting period.