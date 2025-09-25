from .indicators import to_series, rsi, ema, sma, macd, bollinger, atr, obv


def extract_features_from_ohlcv(ohlcv):
    df = to_series(ohlcv)
    close = df['close']
    features = {}
    features['last'] = float(close.iloc[-1])
    features['rsi_14'] = float(rsi(close,14).iloc[-1])
    features['ema50'] = float(ema(close,50).iloc[-1])
    features['ema200'] = float(ema(close,200).iloc[-1])
    macd_line, signal_line, hist = macd(close)
    features['macd'] = float(macd_line.iloc[-1])
    features['macd_signal'] = float(signal_line.iloc[-1])
    sma20, upper, lower = bollinger(close,20,2)
    features['bb_upper'] = float(upper.iloc[-1])
    features['bb_lower'] = float(lower.iloc[-1])
    features['atr_14'] = float(atr(df,14).iloc[-1])
    features['obv'] = float(obv(df).iloc[-1])
    features['vol'] = float(df['vol'].iloc[-1])
    # vol zscore
    vol_mean = df['vol'].rolling(20).mean().iloc[-1]
    vol_std = df['vol'].rolling(20).std().iloc[-1]
    features['vol_z'] = float((features['vol'] - (vol_mean or 0)) / ((vol_std or 1)))
    return features