import time


class Two_min_checker:
    @staticmethod
    def two_minutes_candle_check(kite,breeze, trading_symbol,company_stock_code,quantity):
        time.sleep(1)
        data = breeze.get_historical_data_v2(interval="1minute",
                                             from_date="2024-06-21T13:10:00.000Z",
                                             to_date="2024-06-21T13:12:00.000Z",
                                             stock_code=company_stock_code,
                                             exchange_code="NSE",
                                             product_type="cash")

        # Extracting open and close prices
        open_prices = [entry['open'] for entry in data['Success']]
        close_prices = [entry['close'] for entry in data['Success']]

        colour_list = []

        for i in range(len(open_prices)):
            if close_prices[i] >= open_prices[i]:
                colour_list.append("green")
            else:
                colour_list.append("red")

        buy_price = 210.05
        long_value = float(buy_price) + 0.3
        sell_price = round(long_value, 2)

        colour_list = ['red', 'green', 'green', 'green', 'green', 'red']

        if colour_list[0] == 'red' and colour_list[1] == 'red':
            if last_current_close_price > sell_price:
                kite.place_order(
                    tradingsymbol=trading_symbol,
                    variety="regular",
                    exchange='NSE',
                    transaction_type='SELL',
                    quantity=quantity,
                    order_type='MARKET',
                    product='MIS'
                )
                print("EXECUTING THE CURRENT PRICE")
            else:
                kite.place_order(
                    tradingsymbol=trading_symbol,
                    variety="regular",
                    exchange='NSE',
                    transaction_type='SELL',
                    quantity=quantity,
                    price=sell_price,
                    order_type="LIMIT",
                    product='MIS'
                )
                print("EXECUTING THE LIMIT ORDER")

        else:
            time.sleep(180)
            print("WAITING FOR 3 MINUTES")
