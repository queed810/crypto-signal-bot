import math
from .config import RISK_PER_TRADE


def calc_position_size(account_balance, entry_price, stop_price, risk_per_trade=RISK_PER_TRADE):
    # riesgo absoluto por trade
    risk_money = account_balance * risk_per_trade
    risk_per_unit = abs(entry_price - stop_price)
    if risk_per_unit == 0:
        return 0
    size = risk_money / risk_per_unit
    return math.floor(size)


def calc_sl_tp(entry_price, atr, mode='long'):
    # stop a 1.5 * ATR por defecto; tp 2*ATR
    sl = entry_price - 1.5*atr if mode=='long' else entry_price + 1.5*atr
    tp = entry_price + 2*atr if mode=='long' else entry_price - 2*atr
    return sl, tp