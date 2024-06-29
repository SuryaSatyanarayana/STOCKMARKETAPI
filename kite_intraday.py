from TimeTracker5min import TimeTracker
from breezeConnectivity import BreezeClient
from currentTime import DateTimeConverter
from TimeDiff import TimeConverter
from TimeTracker5min import TimeTracker
import matplotlib.pyplot as plt
from datetime import datetime
import time
import pandas as pd

from get_Instrument_Id import read_instrument_id
from kite import get_api_key
from kite_current_time import CurrentTIme
from kite_time_diff import Kite_TimeConverter
from readStockData import get_trade_by_stock_code
from read_open_position_status import find_first_matching_entry

# STOCK MARKET MY START TIME
start_hour, start_minute = 8, 15

# STOCK MARKET MY END TIME
end_hour, end_minute = 15, 00  # 7:30 PM
Iteration = 1

Api_Count = 0

while True:
    try:
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
            kite = get_api_key()

            print("KITE API CONNECTION ESTABLISHED SUCCESSFULLY")

            trading_symbol = "GAIL"

            instrument_id = read_instrument_id(kite, trading_symbol)

            TimeTracker.run()

            converter = CurrentTIme()
            current_time_in_ist = converter.get_current_ist_time()

            current_time_5_mins_before = Kite_TimeConverter.kite_convert_to_ist(5)
            print("PRINT THE 5 MINS BEFORE THE CURRENT TIME:: ", current_time_5_mins_before)

            current_time_10_mins_before = Kite_TimeConverter.kite_convert_to_ist(10)
            print("PRINT THE 10 MINS BEFORE THE CURRENT TIME:: ", current_time_10_mins_before)

            date_object = datetime.strptime(current_time_5_mins_before, "%Y-%m-%d %H:%M:%S")
            diff_time_seconds_5mins = date_object.second

            date_object = datetime.strptime(current_time_10_mins_before, "%Y-%m-%d %H:%M:%S")
            diff_time_seconds_10mins = date_object.second

            if diff_time_seconds_10mins == 0 and diff_time_seconds_5mins == 0:

                # Wait for 1 minute (60 seconds)
                print("WAITING FOR 1 MINUTE")
                time.sleep(60)

                data = kite.historical_data(instrument_id, current_time_10_mins_before, current_time_in_ist, "5minute")
                last_close_price_5min_candle = data[-1]['close']
                last_high_price_5min_candle = data[-1]['high']

                Api_Count += 1

                colour_list = []

                # Convert data to a DataFrame
                df = pd.DataFrame(data)

                # Create the plot
                fig, ax = plt.subplots()

                for idx, row in df.iterrows():
                    if row['close'] > row['open']:
                        color = 'green'
                    elif row['close'] < row['open']:
                        color = 'red'
                    else:
                        color = 'neutral'

                    # Plot high-low line
                    ax.plot([row['date'], row['date']], [row['low'], row['high']], color='black')

                    # Plot open-close bar
                    if color == 'green':
                        ax.plot([row['date'], row['date']], [row['open'], row['close']], color=color, linewidth=5)
                        colour_list.append("green")
                    elif color == 'red':
                        ax.plot([row['date'], row['date']], [row['open'], row['close']], color=color, linewidth=5)
                        colour_list.append("red")
                    else:
                        ax.plot([row['date'], row['date']], [row['open'], row['close']], color='gray', linewidth=5,
                                linestyle='dashed')

                if colour_list[0] == "red" and colour_list[1] == "green":
                    print("RED GREEN COLOUR CANDLES MATCHED SUCCESSFULLY")
                    converter = CurrentTIme()
                    current_time_in_ist = converter.get_current_ist_time()
                    print("PRINT THE CURRENT TIME:: ", current_time_in_ist)
                    current_time_1_mins_before = Kite_TimeConverter.kite_convert_to_ist(1)
                    print("PRINT 1 MIN BEFORE THE CURRENT TIME:: ", current_time_1_mins_before)
                    time.sleep(1)
                    data2 = kite.historical_data(instrument_id, current_time_1_mins_before, current_time_in_ist, "minute")
                    last_open_price_1min_Candle = data2[0]['open']
                    last_close_price_1min_Candle = data2[0]['close']

                    quantity=1

                    if last_close_price_1min_Candle >= last_high_price_5min_candle:
                        Api_Count += 1
                        kite.place_order(
                            tradingsymbol=trading_symbol,
                            variety="regular",
                            exchange='NSE',
                            transaction_type='BUY',
                            quantity=quantity,
                            order_type='MARKET',
                            product='MIS'
                        )
                        Api_Count += 1
                        result_data, is_matching = find_first_matching_entry(kite, trading_symbol, quantity)
                        while True:
                            if is_matching:
                                print("BUY STOCK SUCCESSFULLY IN PORTFOLIO")
                                break
                            else:
                                print("BUY SIDE STOCK STILL NOT IN OPEN POSITIONS IN PORTFOLIO. RETRYING...")
                                time.sleep(2)
                                result_data, is_matching = find_first_matching_entry(kite, trading_symbol, quantity)
                                Api_Count += 1

                        buy_price = result_data[0]["average_price"]
                        print("EXECUTED BUY ORDER WITH PRICE OF:: ", buy_price)

                        long_value = float(buy_price) + 0.3
                        sell_price = round(long_value, 2)

                        if is_matching:
                            kite.place_order(
                                tradingsymbol=trading_symbol,
                                variety="regular",
                                exchange='NSE',
                                transaction_type='SELL',
                                quantity=quantity,
                                price=sell_price,
                                order_type="LIMIT",
                                product='MIS'
                            )

                        result_data, is_matching = find_first_matching_entry(kite, trading_symbol, 0)

                        while True:
                            if is_matching:
                                print("SELL STOCK SUCCESSFULLY IN PORTFOLIO")
                                break
                            else:
                                print("SELL SIDE STOCK STILL IN OPEN POSITIONS IN PORTFOLIO. RETRYING...")
                                time.sleep(60)
                                result_data, is_matching = find_first_matching_entry(kite, trading_symbol, 0)
                                Api_Count += 1

                        print("EXECUTED SELL ORDER WITH PRICE OF :: ", sell_price)
                        print("TOTAL API COUNTS ::", Api_Count)
                    else:
                        print("LAST 5 MINS CLOSE PRICE IS NOT GREATER THE OPEN PRICE OF NEXT CANDLE")
                else:
                    print("RED GREEN CANDLE NOT MATCHED AS PER THE CURRENT 5 MINS AND 10 MINS TIME FRAME")

        else:
            print("MY JOB IS DONE I AM EXITING THE STOCK MARKET BYE BYE SEE YOU TOMORROW AGAIN")
            break  # Exit the loop if the program should not be running

        print("----------------------------------------------------------------------------------"
              "-------------------------------------END-----------------------------------------"
              "-----------------------------------------------------------------------------------")
    except Exception as e:
        print("An unexpected error occurred and am not exiting the from this while loop:")

    Iteration += 1
