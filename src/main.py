import asyncio
from config.settings import SYMBOL, TIMEFRAME, LIMIT
from src.utils.binance_client import get_klines, test_connection, test_account, buy_solana, sell_solana
from src.utils.telegram_bot import send_message
from src.strategies.moving_average import check_signal
from src.utils.indicators import moving_averages

async def main():
    if not test_connection():
        return
    if not test_account():
        return
    
    last_signal = None # evita repetir ordens

    while True:
        try:
            # Pega dados da Binance
            df = get_klines(SYMBOL, TIMEFRAME, LIMIT)
            df = moving_averages(df, 7, 40)

            # Verifica sinal
            signal = check_signal(df)

            if signal and signal != last_signal:
                if signal == "buy":
                    order = buy_solana(SYMBOL)
                    msg = f"🚀 COMPRA executada em {SYMBOL} (máx $10)"
                elif signal == "sell":
                    order = sell_solana(SYMBOL)
                    msg = f"🔻 VENDA executada em {SYMBOL} (saldo total)"
                else:
                    msg = "⏸️ Nenhum sinal — HOLD"
                
                print(msg)
                await send_message(msg)

                last_signal = signal

            await asyncio.sleep(60)  # Checa a cada 1 minuto sem bloquear o loop

        except Exception as e:
            print(f"Erro: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
