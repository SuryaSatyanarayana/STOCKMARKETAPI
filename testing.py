import json

from breeze_connect import BreezeConnect

from readStockData import get_trade_by_stock_code

breeze = BreezeConnect(api_key="4`32&2Sp2kb2988N68^6!3364324=9D@")

# Generate Session
breeze.generate_session(api_secret="y85q57170j648864136eL24878uZ00S5",
                        session_token="41027635")

company_stock_code = "BANBAR"

print(get_trade_by_stock_code(breeze,company_stock_code))

portfolio_positions = get_trade_by_stock_code(breeze, company_stock_code)
lowest_price = portfolio_positions['Success'][0]['average_price']
print("EXECUTED BUY ORDER WITH PRICE OF:: ", lowest_price)
