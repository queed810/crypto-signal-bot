# src/notifier.py
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

async def send_message(text: str):
    """Envía un mensaje al chat de Telegram configurado en .env"""
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Error: Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en el archivo .env")
        return

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(BASE_URL, data=payload) as resp:
                if resp.status != 200:
                    print(f"⚠️ Error enviando mensaje: {resp.status}")
                    print(await resp.text())
        except Exception as e:
            print(f"⚠️ Excepción al enviar mensaje: {e}")

# Para pruebas rápidas
if __name__ == "__main__":
    asyncio.run(send_message("🚀 Notifier funcionando correctamente."))
