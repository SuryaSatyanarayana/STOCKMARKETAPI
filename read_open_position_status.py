

def find_first_matching_entry(kite,tradingsymbol, quantity):
    data = kite.positions()
    if data['day'][0]['tradingsymbol'] == tradingsymbol and data['day'][0]['quantity'] == quantity:
        return True
    else:
        return False
