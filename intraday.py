from TimeTracker5min import TimeTracker
from breezeConnectivity import BreezeClient
from currentTime import DateTimeConverter
from TimeDiff import TimeConverter
from TimeTracker5min import TimeTracker
import matplotlib.pyplot as plt



breeze= BreezeClient(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5", session_token="40405580")

TimeTracker.run()

converter = DateTimeConverter()
current_time_in_ist = converter.get_current_ist_time()

diff_time=TimeConverter.convert_to_ist(5)


company_stock_code="BANBAR"
data=breeze.get_historical_data_v2(interval="1minute",
                            from_date= diff_time,
                            to_date= current_time_in_ist,
                            stock_code=company_stock_code,
                            exchange_code="NSE",
                            product_type="cash",
                                    )

# Extracting open and close prices
open_prices = [entry['open'] for entry in data['Success']]
close_prices = [entry['close'] for entry in data['Success']]



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





