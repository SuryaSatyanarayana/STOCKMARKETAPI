import time
from datetime import datetime, timedelta

from breeze_connect import BreezeConnect
import matplotlib.pyplot as plt

from currentTime import DateTimeConverter
from kite_current_time import CurrentTIme

company_stock_code = "GAIL"

# Initialize SDK
breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")

# Generate Session
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                        session_token="42919747")

print("BREEZE API CONNECTION ESTABLISHED SUCCESSFULLY")

converter = DateTimeConverter()
current_time_in_ist = converter.get_current_ist_time()

current_time_in_ist = "2024-06-23T17:12:12.000Z"

print(current_time_in_ist)

plt.figure(figsize=(12, 6))

data = breeze.get_historical_data_v2(interval="1minute",
                                     from_date="2024-06-21T13:10:00.000Z",
                                     to_date="2024-06-21T13:12:00.000Z",
                                     stock_code=company_stock_code,
                                     exchange_code="NSE",
                                     product_type="cash")

# Extracting open and close prices
open_prices = [entry['open'] for entry in data['Success']]
close_prices = [entry['close'] for entry in data['Success']]

colour_list = []

for i in range(len(open_prices)):
    if close_prices[i] >= open_prices[i]:
        plt.plot([i, i], [low := open_prices[i], high := close_prices[i]], color='green', linewidth=3)
        plt.plot([i, i], [low, high], marker='o', color='green', markersize=7)
        colour_list.append("green")
    else:
        plt.plot([i, i], [low := close_prices[i], high := open_prices[i]], color='red', linewidth=3)
        plt.plot([i, i], [low, high], marker='o', color='red', markersize=7)
        colour_list.append("red")

buy_price = 210.05
long_value = float(buy_price) + 0.3
sell_price = round(long_value, 2)

colour_list = ['red', 'green', 'green', 'green', 'green', 'red']


if colour_list[0] == 'red' and colour_list[1] == 'red':
    if sell_price > 0:
        print("EXECUTING THE CURRENT PRICE")
    else:
        print("EXECUTING THE LIMIT ORDER")

else:
    time.sleep(180)
    print("WAITING FOR 3 MINUTES")

plt.xlabel('Minute Interval')
plt.ylabel('Price')
plt.title(f'Historical Minute Data for {company_stock_code}')
plt.xticks(range(len(open_prices)), rotation=45)
plt.legend(['Up', 'Down'], loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig('historical_data_plot.png')
plt.show()

# Initial date and time stored in a variable
initial_datetime_str = "2024-06-21 12:05:00"
start_datetime = datetime.strptime(initial_datetime_str, "%Y-%m-%d %H:%M:%S")

# Define the number of iterations (let's say 5 for example)
num_iterations = 5

# Iterate and add 5 minutes in each iteration
for i in range(num_iterations):
    # Add 5 minutes to the current datetime
    current_datetime = start_datetime + timedelta(minutes=i * 5)
    print(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
