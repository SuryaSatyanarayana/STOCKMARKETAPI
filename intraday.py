from email.message import EmailMessage
import ssl
import smtplib

from breeze_connect import BreezeConnect

# Initialize SDK
breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.

import urllib
print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("4`32&2Sp2kb2988N68^6!3364324=9D@"))


# Generate Session
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                        session_token="35538039")

# Generate ISO8601 Date/DateTime String
import datetime
iso_date_string = datetime.datetime.strptime("28/02/2021","%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
iso_date_time_string = datetime.datetime.strptime("28/02/2021 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'

company_stock_code="ITC"
data=breeze.get_historical_data_v2(interval="1minute",
                            from_date= "2024-02-16T15:20:00.000Z",
                            to_date= "2024-02-16T15:25:00.000Z",
                            stock_code=company_stock_code,
                            exchange_code="NSE",
                            product_type="cash",
                                    )

import pandas as pd

print(data)
data2=pd.DataFrame(data['Success'])
print(data2.columns)
print(data2.values)


# Creating all the parameters
sender_email = 'pravallikamedisetti99@gmail.com'
sender_password='lhaz ftfv xtru zuqf'
receiver_email = 'suryaansav1@gmail.com'
subject = 'INTRADAY TRADING ALGORITHM MATCHED FOR THE GIVEN COMPANY ::: ' +company_stock_code
body = data2.values

em = EmailMessage()
em['From'] = sender_email
em['To'] = receiver_email
em['Subject'] = subject
em.set_content(body)

context=ssl.create_default_context()
send=smtplib.SMTP_SSL('smtp.gmail.com',465,context=context)
send.login(sender_email,sender_password)

#send email
send.sendmail(sender_email,receiver_email,em.as_string())




