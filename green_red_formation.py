from email.message import EmailMessage
import ssl
import smtplib

import numpy as np
from breeze_connect import BreezeConnect
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pytz



# Initialize SDK
breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")


# Generate Session
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                        session_token="40438276")

# Get current UTC time
current_utc_time = datetime.utcnow()
# Define Indian Standard Time (IST) timezone
ist_timezone = pytz.timezone('Asia/Kolkata')
# Convert UTC time to IST
current_ist_time = pytz.utc.localize(current_utc_time).astimezone(ist_timezone)
ist_time = current_ist_time.replace(microsecond=0)

# Format the datetime in the desired format
currentTime = ist_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

print(currentTime)


"""
The following code retrieves the current time in UTC, converts it to Indian Standard Time (IST),
and then calculates the time 5 minutes before the current time in IST. Finally, it formats the
resulting datetime object into the specified format, ensuring that the milliseconds (last 3 digits)
are set to zero, and prints it.
"""

current_utc_time = datetime.utcnow()
ist_timezone = pytz.timezone('Asia/Kolkata')
current_ist_time = pytz.utc.localize(current_utc_time).astimezone(ist_timezone)
five_minutes_before = current_ist_time - timedelta(minutes=5)
five_minutes_before_zero_milliseconds = five_minutes_before.replace(microsecond=0)
formatted_datetime = five_minutes_before_zero_milliseconds.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
print(formatted_datetime)

company_stock_code="BANBAR"
data=breeze.get_historical_data_v2(interval="1minute",
                            from_date= formatted_datetime,
                            to_date= currentTime,
                            stock_code=company_stock_code,
                            exchange_code="NSE",
                            product_type="cash",
                                    )


# Extracting open and close prices
open_prices = [entry['open'] for entry in data['Success']]
close_prices = [entry['close'] for entry in data['Success']]

freeze_time=30

# Plotting candles
plt.figure(figsize=(10, 6))

for i in range(len(open_prices)):
    if close_prices[i] > open_prices[i]:
        plt.plot([i, i], [low := open_prices[i], high := close_prices[i]], color='green', linewidth=3)
        plt.plot([i, i], [low, high], marker='o', color='green', markersize=7)


    else:
        plt.plot([i, i], [low := close_prices[i], high := open_prices[i]], color='red', linewidth=3)
        plt.plot([i, i], [low, high], marker='o', color='red', markersize=7)

plt.xlabel('Time Interval')
plt.ylabel('Price')
plt.title('Intraday Candlestick Chart')
plt.grid(True)
plt.savefig('green_red.png')
plt.show()