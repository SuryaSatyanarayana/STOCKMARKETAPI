from email.message import EmailMessage
import ssl
import smtplib

import numpy as np
from breeze_connect import BreezeConnect
import matplotlib.pyplot as plt



# Initialize SDK
breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")


# Generate Session
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                        session_token="40514650")

company_stock_code="BANBAR"
data=breeze.get_historical_data_v2(interval="5minute",
                            from_date= "2024-05-14T11:25:00.000Z",
                            to_date= "2024-05-14T11:30:00.000Z",
                            stock_code=company_stock_code,
                            exchange_code="NSE",
                            product_type="cash")


# Extracting open and close prices
open_prices = [entry['open'] for entry in data['Success']]
low_prices= [entry['low'] for entry in data['Success']]
lowest_price = min(low_prices)
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
        red_colour_counter +=i

if red_colour_counter==2:



plt.xlabel('Time Interval')
plt.ylabel('Price')
plt.title('Intraday Candlestick Chart')
plt.grid(True)
plt.savefig('green_red.png')
plt.show()




# import pandas as pd
# from ema_21 import calculate_ema_21
#
#
# closing_prices = close_prices
# closing_prices_series = pd.Series(closing_prices, index=pd.date_range(start='2024-04-01 09:30:00', periods=len(closing_prices), freq='5min'))
# ema_21 = calculate_ema_21(closing_prices_series, window=21)
#
# # Plotting
# import matplotlib.pyplot as plt
#
# plt.figure(figsize=(10, 6))
# plt.plot(closing_prices_series, label='Closing Prices', color='blue')
# plt.plot(ema_21, label='EMA (21 days)', color='red')
# plt.title('Intraday Closing Prices and Exponential Moving Average (EMA)')
# plt.xlabel('Time')
# plt.ylabel('Price')
# plt.legend()
# plt.grid(True)
# plt.savefig('sample_graph.png')
# plt.show()


# from ema_9 import calculate_ema_9
# closing_prices = [...]  # Your intraday closing prices here
# closing_prices_series = pd.Series(closing_prices, index=pd.date_range(start='2024-04-21 09:30:00', periods=len(closing_prices), freq='15T'))
# ema_9 = calculate_ema_9(closing_prices_series, window=9)
#
# from ema_150 import calculate_ema_150
#
# closing_prices = [...]  # Your intraday closing prices here
# closing_prices_series = pd.Series(closing_prices, index=pd.date_range(start='2024-04-21 09:30:00', periods=len(closing_prices), freq='15T'))
# ema_150 = calculate_ema_150(closing_prices_series, window=150)
#
#
#
# # Creating all the parameters
# sender_email = 'pravallikamedisetti99@gmail.com'
# sender_password='lhaz ftfv xtru zuqf'
# receiver_email = 'suryaansav1@gmail.com'
# subject = 'INTRADAY TRADING ALGORITHM MATCHED FOR THE GIVEN COMPANY ::: ' +company_stock_code
#
# em = EmailMessage()
# em['From'] = sender_email
# em['To'] = receiver_email
# em['Subject'] = subject
#
# context=ssl.create_default_context()
# send=smtplib.SMTP_SSL('smtp.gmail.com',465,context=context)
# send.login(sender_email,sender_password)
#
# #send email
# send.sendmail(sender_email,receiver_email,em.as_string())




