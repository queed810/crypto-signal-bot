import sqlite3
from .config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS signals
    (id INTEGER PRIMARY KEY, ts INTEGER, symbol TEXT, side TEXT, score REAL, confidence REAL, features TEXT)''')
    conn.commit()
    conn.close()


def save_signal(ts, symbol, side, score, confidence, features_json):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO signals (ts,symbol,side,score,confidence,features) VALUES (?,?,?,?,?,?)',
    (ts, symbol, side, score, confidence, features_json))
    conn.commit()
    conn.close()