import pytz
from datetime import datetime


class CurrentTIme:
    def __init__(self):
        # Initialize the DateTimeConverter class with UTC and IST timezones
        self.utc_timezone = pytz.utc
        self.ist_timezone = pytz.timezone('Asia/Kolkata')

    def get_current_ist_time(self):
        # Get the current UTC time
        current_utc_time = datetime.utcnow()

        # Convert the current UTC time to IST timezone
        current_ist_time = self.utc_timezone.localize(current_utc_time).astimezone(self.ist_timezone)

        # Round off microseconds to zero
        ist_time = current_ist_time.replace(microsecond=0)

        # Format the IST time in ISO 8601 format with milliseconds and 'Z' indicating UTC
        formatted_time = ist_time.strftime("%Y-%m-%d %H:%M:%S")

        # Print and return the formatted time
        print(formatted_time)
        return formatted_time
