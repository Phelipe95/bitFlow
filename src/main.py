import asyncio
from config.settings import TRADE_SYMBOL, INTERVAL, LIMIT
from src.utils.binance_client import get_klines
from src.utils.telegram_bot import send_message
from src.strategies.moving_average import check_signal
from src.utils.indicators import moving_averages
import time

if __name__ == "__main__":
    while True:
        try:
            # Pega dados da Binance
            df = get_klines(TRADE_SYMBOL, INTERVAL, LIMIT)
            df = moving_averages(df, 7, 40)

            # Verifica sinal
            signal = check_signal(df)

            if signal:
                msg = f"🚨 Sinal de {signal} em {TRADE_SYMBOL} no gráfico {INTERVAL}"
                print(msg)
                send_message(msg)

            time.sleep(60)  # espera 1 minuto para atualizar

        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(60)
