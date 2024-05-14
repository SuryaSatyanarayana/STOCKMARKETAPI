from TimeTracker5min import TimeTracker
from breezeConnectivity import BreezeClient
from currentTime import DateTimeConverter
from TimeDiff import TimeConverter
from TimeTracker5min import TimeTracker
import matplotlib.pyplot as plt
from datetime import datetime
from breeze_connect import BreezeConnect




# Initialize SDK
breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")

# Generate Session
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                        session_token="40514650")

print("BREEZE API CONNECTION ESTABILISHED SUCCESSFULLY")

# TimeTracker.run()
#
# print("PRINT THE CURRENT TIME")
# converter = DateTimeConverter()
# current_time_in_ist = converter.get_current_ist_time()
# print("PRINT THE 5 MINS BEFORE THE CURRENT TIME")
#
# current_time_5_mins_before=TimeConverter.convert_to_ist(5)
# current_time_10_mins_before=TimeConverter.convert_to_ist(10)
#
# date_object = datetime.strptime(current_time_in_ist, "%Y-%m-%dT%H:%M:%S.%fZ")
# current_time_seconds = date_object.second
#
# date_object = datetime.strptime(current_time_5_mins_before, "%Y-%m-%dT%H:%M:%S.%fZ")
# diff_time_seconds_5mins = date_object.second
#
# date_object = datetime.strptime(current_time_10_mins_before, "%Y-%m-%dT%H:%M:%S.%fZ")
# diff_time_seconds_10mins = date_object.second
#
# if diff_time_seconds_10mins==0 and diff_time_seconds_5mins==0 :

company_stock_code="BANBAR"
data=breeze.get_historical_data_v2(interval="5minute",
                            from_date= "2024-05-14T11:25:00.000Z",
                            to_date= "2024-05-14T11:30:00.000Z",
                            stock_code=company_stock_code,
                            exchange_code="NSE",
                            product_type="cash")

# Extracting open and close prices
open_prices = [entry['open'] for entry in data['Success']]
close_prices = [entry['close'] for entry in data['Success']]


red_colour_counter = 1



# Plotting candles
plt.figure(figsize=(10, 6))

for i in range(len(open_prices)):
    if close_prices[i] > open_prices[i]:
        plt.plot([i, i], [low := open_prices[i], high := close_prices[i]], color='green', linewidth=3)
        plt.plot([i, i], [low, high], marker='o', color='green', markersize=7)
    else:
        plt.plot([i, i], [low := close_prices[i], high := open_prices[i]], color='red', linewidth=3)
        plt.plot([i, i], [low, high], marker='o', color='red', markersize=7)
        red_colour_counter += i

if red_colour_counter==2:
    print("TWO RED COLOUR CANDLES MATCHED SUCCESSFULLY")
    print("PRINT THE CURRENT TIME")
    converter = DateTimeConverter()
    current_time_in_ist = converter.get_current_ist_time()
    current_time_1_mins_before = TimeConverter.convert_to_ist(1)
    data = breeze.get_historical_data_v2(interval="1second",
                                         from_date=current_time_1_mins_before,
                                         to_date=current_time_in_ist,
                                         stock_code=company_stock_code,
                                         exchange_code="NSE",
                                         product_type="cash")
    low_prices = [entry['low'] for entry in data['Success']]
    lowest_price = min(low_prices)
    stoploss_price=lowest_price+0.2
    print("BUYING THE STOCK NOW WITH PRICE OF: "+lowest_price)
    breeze.place_order(stock_code=company_stock_code,
                       exchange_code="NSE",
                       product="cash",
                       action="buy",
                       order_type="limit",
                       stoploss=stoploss_price,
                       quantity="1",
                       price=lowest_price,
                       validity="day"
                       )
    breeze.get_portfolio_positions()


plt.xlabel('Time Interval')
plt.ylabel('Price')
plt.title('Intraday Candlestick Chart')
plt.grid(True)
plt.savefig('green_red.png')
plt.show()





