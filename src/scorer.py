import json
from .config import EMA_FAST, EMA_SLOW, RSI_PERIOD, VOL_MULTIPLIER


# regla combinada + placeholder ML


def rule_score(features):
    score = 0.0
    # tendencia (EMA fast vs slow)
    if features['ema50'] > features['ema200']:
        score += 0.25
    else:
        score -= 0.25
        # RSI
        r = features['rsi_14']
    if r < 30:
        score += 0.25
    elif r > 70:
        score -= 0.25
        # MACD cross
    if features['macd'] > features['macd_signal']:
        score += 0.15
    else:
        score -= 0.15
        # volumen
    if features['vol_z'] > 1.5:
        score += 0.2
        # bollinger
        price = features['last']
    if price <= features['bb_lower']:
        score += 0.15
    if price >= features['bb_upper']:
        score -= 0.15
        # normalize to 0-1
    score = max(-1, min(1, score))
    normalized = (score + 1)/2
    return normalized


# placeholder model interface (si entrenas un ML, guarda en models/model.pkl)
def model_predict_proba(features_dict):
# por ahora no hay modelo; devuelve None
    return None


def combined_score(features):
    r = rule_score(features)
    m = model_predict_proba(features)
    if m is None:
        return {'score': r, 'confidence': r}
        combined = 0.6*m + 0.4*r
        return {'score': combined, 'confidence': m}