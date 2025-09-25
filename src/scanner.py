import asyncio, ccxt.async_support as ccxt
import time
from typing import List
from .config import EXCHANGE_ID, CANDLE_LIMIT, TIMEFRAMES, MAX_CONCURRENCY

exchange = None

async def init_exchange(api_key=None, secret=None):
    global exchange
    exchange = getattr(ccxt, EXCHANGE_ID)({
        'enableRateLimit': True,
    })
    # puedes setear apiKey/secret si hará trading
    # exchange.apiKey = api_key; exchange.secret = secret

async def fetch_ohlcv(symbol: str, timeframe="5m", limit=200):
    global exchange
    try:
        data = await exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        # cada item: [ts, open, high, low, close, vol]
        return data
    except Exception as e:
        print("fetch_ohlcv error", symbol, e)
        return []

async def fetch_orderbook(symbol: str, depth=10):
    global exchange
    try:
        ob = await exchange.fetch_order_book(symbol, limit=depth)
        return ob
    except Exception as e:
        print("fetch_orderbook error", symbol, e)
        return {}

async def scan_symbols(symbols: List[str], timeframe="5m"):
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    results = {}

    async def worker(sym):
        async with sem:
            ohlcv = await fetch_ohlcv(sym, timeframe, CANDLE_LIMIT)
            ob = await fetch_orderbook(sym, depth=20)
            results[sym] = {"ohlcv": ohlcv, "orderbook": ob}
            await asyncio.sleep(0.05)  # small pause to respect rate
    tasks = [asyncio.create_task(worker(s)) for s in symbols]
    await asyncio.gather(*tasks)
    return results

async def close():
    global exchange
    if exchange:
        await exchange.close()
