class NumberComparator:
    def check_number(buy_price,current_price):
        if buy_price > current_price:
            print("CURRENT PRICE IS LESS THAN THE BUY PRICE LOSS SIDE")
            return buy_price
        elif buy_price < buy_price+0.5:
            print("STAGE 1 STARTED SUCCESSFULLY FOR 0.5")
            return buy_price
        elif buy_price < buy_price+1.0:
            print("STAGE 1 STARTED SUCCESSFULLY FOR 1.0")
            return buy_price
        elif buy_price < buy_price+1.5:
            print("STAGE 1 STARTED SUCCESSFULLY FOR 1.5")
            return buy_price
        elif buy_price < buy_price+2.0:
            print("STAGE 1 STARTED SUCCESSFULLY FOR 2.0")
            return buy_price
        else:
            return buy_price
