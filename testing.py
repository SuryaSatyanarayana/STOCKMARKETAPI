from TimeTracker5min import TimeTracker
from breezeConnectivity import BreezeClient
from currentTime import DateTimeConverter
from TimeDiff import TimeConverter
from TimeTracker5min import TimeTracker
import matplotlib.pyplot as plt
from datetime import datetime
from breeze_connect import BreezeConnect
import time
import json

from readStockData import get_trade_by_stock_code

#STOCK MARKET MY START TIME
start_hour, start_minute = 7, 15

#STOCK MARKET MY END TIME
end_hour, end_minute = 23, 50  # 7:30 PM
Iteration = 1
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
                                session_token="41308241")

        print("BREEZE API CONNECTION ESTABLISHED SUCCESSFULLY")

        company_stock_code = "GAIL"

        # time.sleep(120)

        converter = DateTimeConverter()
        current_time_in_ist = converter.get_current_ist_time()
        print("PRINT THE CURRENT TIME:: ", current_time_in_ist)
        current_time_1_mins_before = TimeConverter.convert_to_ist(1)
        print("PRINT 1 MIN BEFORE THE CURRENT TIME:: ", current_time_1_mins_before)
        data = breeze.get_historical_data_v2(interval="1second",
                                             from_date="2024-05-18T12:05:00.000Z",
                                             to_date="2024-05-18T12:06:00.000Z",
                                             stock_code=company_stock_code,
                                             exchange_code="NSE",
                                             product_type="cash")
        records = data['Success']

        # Access the last record in the list
        last_record = records[-1]

        # Extract the 'datetime' and 'open' values
        datetime_value = last_record['datetime']
        open_value = last_record['open']

        sell_price = float(open_value)+0.2

        # Print the values
        print("Datetime:", datetime_value)
        print("Open:", open_value)

        print("sell:", sell_price)


        breeze.place_order(stock_code=company_stock_code,
                           exchange_code="NSE",
                           product="cash",
                           action="buy",
                           order_type="market",
                           stoploss="",
                           quantity="1",
                           price="",
                           validity="day",
                           )

        portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)
        is_active = False
        while portfolio_positions.get('Success') is None:
            if portfolio_positions.get('Success') is not None:
                print("BUY STOCK SUCCESSFULLY IN PORTFOLIO")
                is_active = True
                break
            else:
                print("BUY SIDE STOCK STILL NOT IN OPEN POSITIONS IN PORTFOLIO. RETRYING...")
                time.sleep(30)
                portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)

        lowest_price = portfolio_positions['Success'][0]['average_price']
        is_active = True
        print("EXECUTED BUY ORDER WITH PRICE OF:: ", lowest_price)
        selling_price = float(lowest_price) + 0.20
        print("EXECUTED SELL ORDER WITH PRICE OF :: ", selling_price)

        if is_active:
            breeze.place_order(stock_code=company_stock_code,
                               exchange_code="NSE",
                               product="cash",
                               action="sell",
                               order_type="limit",
                               stoploss="",
                               quantity="1",
                               price=selling_price,
                               validity="day",
                               )

        portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)
        is_active = False

        while portfolio_positions.get('Success') is not None:
            if portfolio_positions.get('Success') is None:
                print("SELL STOCK SUCCESSFULLY FROM PORTFOLIO")
                is_active = True
                break
            else:
                print("SELL SIDE STOCK STILL IN OPEN POSITIONS IN PORTFOLIO. RETRYING...")
                time.sleep(30)
                portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)

        print("EXECUTED SELL ORDER WITH PRICE OF :: ", selling_price)

    else:
        print("MY JOB IS DONE I AM EXITING THE STOCK MARKET BYE BYE SEE YOU TOMORROW AGAIN")
        break  # Exit the loop if the program should not be running
