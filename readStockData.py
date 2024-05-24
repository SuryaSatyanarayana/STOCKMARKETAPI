def get_trade_by_stock_code(brz, stock_code):
    data=brz.get_portfolio_positions()
    try:
        success_trades = data.get('Success', [])
        for trade in success_trades:
            if trade.get('stock_code') == stock_code:
                return {"Success": [trade]}
        return {"Success": None}
    except Exception:
        return {"Success": None}