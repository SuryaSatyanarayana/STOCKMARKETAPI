# Initialize SDK
from get_Instrument_Id import read_instrument_id
from kite import get_api_key
from kite_current_time import CurrentTIme
from kite_time_diff import Kite_TimeConverter

kite = get_api_key()

trading_symbol = "GAIL"

instrument_id = read_instrument_id(kite, trading_symbol)

converter = CurrentTIme()
current_time_in_ist = converter.get_current_ist_time()

current_time_5_mins_before = Kite_TimeConverter.kite_convert_to_ist(5)
print("PRINT THE 5 MINS BEFORE THE CURRENT TIME:: ", current_time_5_mins_before)

current_time_10_mins_before = Kite_TimeConverter.kite_convert_to_ist(10)
print("PRINT THE 10 MINS BEFORE THE CURRENT TIME:: ", current_time_10_mins_before)

data = kite.historical_data(instrument_id, "2024-06-13 12:20:00", "2024-06-13 12:21:00", "5minute")

print(data)