from breeze_connect import BreezeConnect

from TimeDiff import TimeConverter
from currentTime import DateTimeConverter

# Initialize SDK
breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")

# Generate Session
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                        session_token="42470901")

converter = DateTimeConverter()
current_time_in_ist = converter.get_current_ist_time()
print("PRINT THE CURRENT TIME:: ", current_time_in_ist)
current_time_1_mins_before = TimeConverter.convert_to_ist(1)

company_stock_code = "GAIL"

data = breeze.get_historical_data_v2(interval="1second",
                                     from_date=current_time_1_mins_before,
                                     to_date=current_time_in_ist,
                                     stock_code=company_stock_code,
                                     exchange_code="NSE",
                                     product_type="cash")
print(data)


