# src/config.py
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# ====== CONFIGURACIÓN DEL BOT ======
BOT_NAME = "CryptoSignalBot"
VERSION = "1.0"

# ====== CONFIGURACIÓN DE EXCHANGE ======
# ID de exchange para CCXT (ej: "binance", "bybit", "kraken")
EXCHANGE_ID = os.getenv("EXCHANGE_ID", "binance")

# Límite de velas a descargar en cada consulta
CANDLE_LIMIT = 500  

# Timeframes a analizar (puedes modificar según estrategia)
TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
    "1h"
]

# Máxima concurrencia de requests (para no saturar el exchange)
MAX_CONCURRENCY = 5

# ====== CONFIGURACIÓN DE TELEGRAM ======
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ====== GESTIÓN DE RIESGO ======
RISK_PER_TRADE = 0.01     # 1% del capital
MAX_OPEN_TRADES = 3       # máximo de trades abiertos al mismo tiempo
STOP_LOSS_PCT = 0.02      # 2% stop loss
TAKE_PROFIT_PCT = 0.05    # 5% take profit

# ====== CRYPTOS A ANALIZAR ======
# Puedes agregar más símbolos soportados por tu exchange
SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "SOL/USDT",
    "XRP/USDT"
]


# ====== FILTROS DE SEÑALES ======
# Puntuación mínima de reglas técnicas para validar trade
RULE_SCORE_THRESHOLD = 0.7   # 70%

# Confianza mínima del modelo ML para validar trade
MODEL_CONF_THRESHOLD = 0.6   # 60%

# ====== BASE DE DATOS LOCAL ======
# Ruta al archivo SQLite donde se guardarán señales
DB_PATH = os.path.join(os.path.dirname(__file__), "signals.db")
