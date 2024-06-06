

def find_first_matching_entry(kite,tradingsymbol, quantity):
    data = kite.positions()
    lastData = [item for item in data["day"] if item.get("tradingsymbol") == tradingsymbol and item.get("quantity") == quantity]
    return lastData, bool(lastData)
