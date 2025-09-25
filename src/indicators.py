import numpy as np
import pandas as pd


# funciones vectorizadas y robustas


def to_series(ohlcv):
    df = pd.DataFrame(ohlcv, columns=['ts','open','high','low','close','vol'])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df.set_index('ts', inplace=True)
    df = df.astype(float)
    return df


def sma(series, period=20):
    return series.rolling(period).mean()


def ema(series, period=20):
    return series.ewm(span=period, adjust=False).mean()


def rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.rolling(period).mean()
    ma_down = down.rolling(period).mean()
    rs = ma_up / ma_down.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(series, fast=12, slow=26, signal=9):
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def bollinger(series, period=20, std_mult=2):
    sma_ = sma(series, period)
    std = series.rolling(period).std()
    upper = sma_ + std_mult * std
    lower = sma_ - std_mult * std
    return sma_, upper, lower


def atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def obv(df):
    sign = np.sign(df['close'].diff()).fillna(0)
    return (df['vol'] * sign).cumsum()