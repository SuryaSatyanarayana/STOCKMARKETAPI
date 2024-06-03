def read_instrument_id(kite,query):
    instruments = kite.instruments()
    instrument_id =None
    for instrument in instruments:
        if instrument['tradingsymbol'] == query:
            instrument_id = instrument['instrument_token']
            print("Instrument ID for", query, ":", instrument_id)
            return instrument_id
            break
    else:
        print("No instrument found for", query)
        return instrument_id