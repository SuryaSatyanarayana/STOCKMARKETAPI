import pytz
from datetime import datetime, timedelta

class TimeConverter:
    @staticmethod
    def convert_to_ist(input_time):
        # Get the current UTC time
        current_utc_time = datetime.utcnow()

        # Define the IST timezone
        ist_timezone = pytz.timezone('Asia/Kolkata')

        # Convert current UTC time to IST
        current_ist_time = pytz.utc.localize(current_utc_time).astimezone(ist_timezone)

        # Subtract minutes from the current IST time
        five_minutes_before = current_ist_time - timedelta(minutes=input_time)

        # Remove microseconds from the resulting time
        five_minutes_before_zero_milliseconds = five_minutes_before.replace(microsecond=0)

        # Format the datetime as ISO 8601 format
        formatted_datetime = five_minutes_before_zero_milliseconds.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

        print(formatted_datetime)
        return formatted_datetime
