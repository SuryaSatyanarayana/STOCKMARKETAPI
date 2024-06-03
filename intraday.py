from TimeTracker5min import TimeTracker
from breezeConnectivity import BreezeClient
from currentTime import DateTimeConverter
from TimeDiff import TimeConverter
from TimeTracker5min import TimeTracker
import matplotlib.pyplot as plt
from datetime import datetime
from breeze_connect import BreezeConnect
import time

from readStockData import get_trade_by_stock_code

#STOCK MARKET MY START TIME
start_hour, start_minute = 9, 15

#STOCK MARKET MY END TIME
end_hour, end_minute = 14, 45  # 7:30 PM
Iteration = 1

Api_Count = 0

while True:
    print("----------------------------------------------------------------------------------"
          "-------------------------------------START--->", Iteration, "-----------------------------------------"
                                                                       "-----------------------------------------------------------------------------------")
    # Get the current time
    current_time = time.localtime()

    # Extract the current hour and minute
    current_hour = current_time.tm_hour
    current_minute = current_time.tm_min

    # Check if the current time is between start and end times
    if (current_hour > start_hour or (current_hour == start_hour and current_minute >= start_minute)) and \
            (current_hour < end_hour or (current_hour == end_hour and current_minute <= end_minute)):

        # Initialize SDK
        breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")

        # Generate Session
        breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                                session_token="41515050")

        print("BREEZE API CONNECTION ESTABLISHED SUCCESSFULLY")

        TimeTracker.run()

        converter = DateTimeConverter()
        current_time_in_ist = converter.get_current_ist_time()

        current_time_5_mins_before = TimeConverter.convert_to_ist(5)
        print("PRINT THE 5 MINS BEFORE THE CURRENT TIME:: ", current_time_5_mins_before)

        current_time_10_mins_before = TimeConverter.convert_to_ist(10)
        print("PRINT THE 10 MINS BEFORE THE CURRENT TIME:: ", current_time_10_mins_before)

        date_object = datetime.strptime(current_time_5_mins_before, "%Y-%m-%dT%H:%M:%S.%fZ")
        diff_time_seconds_5mins = date_object.second

        date_object = datetime.strptime(current_time_10_mins_before, "%Y-%m-%dT%H:%M:%S.%fZ")
        diff_time_seconds_10mins = date_object.second

        if diff_time_seconds_10mins == 0 and diff_time_seconds_5mins == 0:

            company_stock_code = "GAIL"

            # Wait for 1 minute (60 seconds)
            print("WAITING FOR 1 MINUTE")
            time.sleep(60)

            data = breeze.get_historical_data_v2(interval="5minute",
                                                 from_date=current_time_10_mins_before,
                                                 to_date=current_time_5_mins_before,
                                                 stock_code=company_stock_code,
                                                 exchange_code="NSE",
                                                 product_type="cash")

            Api_Count +=1

            # Extracting open and close prices
            open_prices = [entry['open'] for entry in data['Success']]
            close_prices = [entry['close'] for entry in data['Success']]

            colour_list = []

            for i in range(len(open_prices)):
                if close_prices[i] > open_prices[i]:
                    plt.plot([i, i], [low := open_prices[i], high := close_prices[i]], color='green', linewidth=3)
                    plt.plot([i, i], [low, high], marker='o', color='green', markersize=7)
                    colour_list.append("green")
                else:
                    plt.plot([i, i], [low := close_prices[i], high := open_prices[i]], color='red', linewidth=3)
                    plt.plot([i, i], [low, high], marker='o', color='red', markersize=7)
                    colour_list.append("red")

            if colour_list[0] == "red" and colour_list[1] == "green":
                print("RED GREEN COLOUR CANDLES MATCHED SUCCESSFULLY")
                converter = DateTimeConverter()
                current_time_in_ist = converter.get_current_ist_time()
                print("PRINT THE CURRENT TIME:: ", current_time_in_ist)
                current_time_1_mins_before = TimeConverter.convert_to_ist(1)
                print("PRINT 1 MIN BEFORE THE CURRENT TIME:: ", current_time_1_mins_before)
                data = breeze.get_historical_data_v2(interval="1second",
                                                     from_date=current_time_1_mins_before,
                                                     to_date=current_time_in_ist,
                                                     stock_code=company_stock_code,
                                                     exchange_code="NSE",
                                                     product_type="cash")
                Api_Count += 1

                records = data['Success']

                # Access the last record in the list
                last_record = records[-1]

                # Extract the 'open' values
                buy_price = last_record['open']

                sell_price = float(buy_price) + 0.2

                breeze.place_order(stock_code=company_stock_code,
                                   exchange_code="NSE",
                                   product="cash",
                                   action="buy",
                                   order_type="limit",
                                   stoploss="",
                                   quantity="1",
                                   price=buy_price,
                                   validity="day",
                                   )
                Api_Count += 1

                portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)
                is_active = False
                while portfolio_positions.get('Success') is None:
                    if portfolio_positions.get('Success') is not None:
                        print("BUY STOCK SUCCESSFULLY IN PORTFOLIO")
                        is_active = True
                        break
                    else:
                        print("BUY SIDE STOCK STILL NOT IN OPEN POSITIONS IN PORTFOLIO. RETRYING...")
                        time.sleep(3)
                        portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)
                        Api_Count += 1

                # lowest_price = portfolio_positions['Success'][0]['average_price']
                is_active = True
                print("EXECUTED BUY ORDER WITH PRICE OF:: ", buy_price)

                if is_active:
                    breeze.place_order(stock_code=company_stock_code,
                                       exchange_code="NSE",
                                       product="cash",
                                       action="sell",
                                       order_type="limit",
                                       stoploss="",
                                       quantity="1",
                                       price=sell_price,
                                       validity="day",
                                       )

                portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)
                is_active = False
                Api_Count += 1

                while portfolio_positions.get('Success') is not None:
                    if portfolio_positions.get('Success') is None:
                        print("SELL STOCK SUCCESSFULLY FROM PORTFOLIO")
                        is_active = True
                        break
                    else:
                        print("SELL SIDE STOCK STILL IN OPEN POSITIONS IN PORTFOLIO. RETRYING...")
                        time.sleep(60)
                        portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)
                        Api_Count += 1

                print("EXECUTED SELL ORDER WITH PRICE OF :: ", sell_price)
                print("TOTAL API COUNTS ::", Api_Count)
            else:
                print("RED GREEN CANDLE NOT MATCHED AS PER THE CURRENT 5 MINS AND 10 MINS TIME FRAME")

    else:
        print("MY JOB IS DONE I AM EXITING THE STOCK MARKET BYE BYE SEE YOU TOMORROW AGAIN")
        break  # Exit the loop if the program should not be running

    print("----------------------------------------------------------------------------------"
          "-------------------------------------END-----------------------------------------"
          "-----------------------------------------------------------------------------------")
    Iteration += 1
