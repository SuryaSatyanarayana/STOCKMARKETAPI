from read_open_position_status import find_first_matching_entry

from kite import get_api_key

kite = get_api_key()

# Retrieve open positions

tradingsymbol="BEL"

read = find_first_matching_entry(kite,tradingsymbol,1)

print(read)

while read:
    print("text")