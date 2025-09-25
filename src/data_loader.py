import ccxt
import asyncio
from typing import List
from .config import EXCHANGE_ID, KLINE_LIMIT


exchange = None


async def init_exchange(api_key=None, secret=None):
    global exchange
    exchange = getattr(ccxt, EXCHANGE_ID)({
    'enableRateLimit': True,
    })
# si vas a ejecutar en testnet, configura aquí


async def fetch_ohlcv(symbol, timeframe='5m', limit=KLINE_LIMIT):
    try:
        return await exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except Exception as e:
        print('fetch_ohlcv error', symbol, e)
        return []


async def close():
    global exchange
    if exchange:
        await exchange.close()