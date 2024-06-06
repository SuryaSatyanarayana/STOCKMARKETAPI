from get_Instrument_Id import read_instrument_id
from kite_current_time import CurrentTIme
from kite_time_diff import Kite_TimeConverter
from read_open_position_status import find_first_matching_entry
import json
from kite import get_api_key

kite = get_api_key()

# Retrieve open positions

trading_symbol = "GAIL"

instrument_id = read_instrument_id(kite, trading_symbol)

converter = CurrentTIme()
current_time_in_ist = converter.get_current_ist_time()
print("PRINT THE CURRENT TIME:: ", current_time_in_ist)
current_time_1_mins_before = Kite_TimeConverter.kite_convert_to_ist(1)
print("PRINT 1 MIN BEFORE THE CURRENT TIME:: ", current_time_1_mins_before)

from_date = "2024-06-05 12:45:00"
to_date = "2024-06-05 12:55:00"

f, is_matching=find_first_matching_entry(kite,"GAIL","-1")

print(f)
print(is_matching)

buy = kite.positions()

ram_data = [item for item in buy["day"] if item.get("tradingsymbol") == "RAM" and item.get("quantity") == -1]

if ram_data:
    print("Data present  ", ram_data)
    print(ram_data[0]["average_price"])
else:
    print("no data")
