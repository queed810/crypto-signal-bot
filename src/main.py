# src/main.py
import asyncio
from src import scanner, signal_manager, notifier, config

async def main():
    # Mensaje de arranque
    await notifier.send_message("✅ Bot iniciado correctamente en tu PC.")

    # Bucle principal
    while True:
        try:
            # 1. Escanear el mercado
            market_data = await scanner.scan_market()

            # 2. Generar señales
            signals = signal_manager.generate_signals(market_data)

            # 3. Enviar señales a Telegram si existen
            if signals:
                for sig in signals:
                    msg = f"""
📊 Señal detectada:
🔹 Par: {sig['symbol']}
🔹 Acción: {sig['action']}
🔹 Precio: {sig['price']}
🔹 Confianza: {sig['confidence']}%
"""
                    await notifier.send_message(msg)

        except Exception as e:
            await notifier.send_message(f"⚠️ Error en ejecución: {e}")

        # Espera antes del siguiente ciclo (ej: 60s)
        await asyncio.sleep(config.SCAN_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
