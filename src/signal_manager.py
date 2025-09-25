import time, json
from .config import RULE_SCORE_THRESHOLD, MODEL_CONF_THRESHOLD
from .storage import save_signal
from .notifier import send_telegram

# cooldowns & dedupe
last_signal_ts = {}  # symbol -> ts

COOLDOWN_SECONDS = 30 * 60  # 30 min cooldown by default

def can_emit(symbol):
    last = last_signal_ts.get(symbol)
    if last is None:
        return True
    return (time.time() - last) > COOLDOWN_SECONDS

def emit_signal(symbol, side, score, confidence, features):
    if not can_emit(symbol):
        return False
    # save and notify
    ts = int(time.time())
    save_signal(ts, symbol, side, score, confidence, json.dumps(features))
    msg = f"📡 <b>Señal</b>\nPar: {symbol}\nSide: {side}\nScore: {score:.3f}\nConf: {confidence:.3f}"
    # añadir SL/TP sugerido
    sl = features.get('atr_14', 0) * 1.5
    tp = features.get('atr_14', 0) * 2
    msg += f"\nSL sugerido: {sl:.6f}\nTP sugerido: {tp:.6f}"
    send_telegram(msg)
    last_signal_ts[symbol] = ts
    return True
