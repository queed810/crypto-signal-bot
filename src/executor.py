import ccxt
from .config import EXCHANGE_ID


# Este módulo solo envía órdenes en paper/testnet si config lo permite.
# En este MVP no ejecutaremos órdenes reales sin tu confirmación.


exchange = None


def init_exec(api_key=None, secret=None):
    global exchange
    exchange = getattr(ccxt, EXCHANGE_ID)({
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    })


def place_order(symbol, side, amount, price=None, type='market'):
    # wrapper simple
    if exchange is None:
        raise Exception("Exchange not initialized")
    if type=='market':
        return exchange.create_market_order(symbol, side, amount)
    else:
        return exchange.create_order(symbol, type, side, amount, price)