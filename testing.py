import json
import matplotlib.pyplot as plt


from breeze_connect import BreezeConnect

from readStockData import get_trade_by_stock_code

breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")

# Generate Session
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                        session_token="41203953")

company_stock_code = "BANBAR"
data=breeze.get_historical_data_v2(interval="1second",
                            from_date= "2024-05-24T15:20:00.000Z",
                            to_date= "2024-05-24T15:21:00.000Z",
                            stock_code=company_stock_code,
                            exchange_code="NSE",
                            product_type="cash")

 # Extracting open and close prices
open_prices = [entry['open'] for entry in data['Success']]
low_prices= [entry['low'] for entry in data['Success']]
lowest_price = min(low_prices)
close_prices = [entry['close'] for entry in data['Success']]

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
plt.savefig('test.png')
