import asyncio
import logging
from config.settings import SYMBOL, TIMEFRAME, LIMIT
from src.utils.binance_client import get_klines, test_connection, test_account, buy_solana, sell_solana, client
from src.utils.telegram_bot import send_message
from src.strategies.moving_average import check_signal
from src.utils.indicators import moving_averages

logging.basicConfig(
    filename="trade_bot.log", # Arquivo de saída
    level=logging.INFO, # Nível mínimo: INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

async def main():
    if not test_connection():
        return
    if not test_account():
        return
    
    last_signal = None # evita repetir ordens
    last_buy_price = None # preço da última compra
    last_buy_qty = None # quantidade comprada

    while True:
        try:
            # Pega dados da Binance
            df = get_klines(SYMBOL, TIMEFRAME, LIMIT)
            df = moving_averages(df, 7, 40)

            # Verifica sinal
            signal = check_signal(df)
            price = float(client.get_symbol_ticker(symbol=SYMBOL)["price"])

            if signal and signal != last_signal:
                if signal == "BUY":
                    order = buy_solana(SYMBOL)
                    if order: # pega a quantidade comprada e o preço
                        executed_qty = float(order["executeQty"])
                        last_buy_qty = executed_qty
                        last_buy_price = price
                        msg = f"🚀 COMPRA executada em {SYMBOL} a {price:.2f} (máx $10)"
                elif signal == "SELL" and last_buy_price:
                    order = sell_solana(SYMBOL)
                    if order:
                        executed_qty = float(order["executeQty"])
                        sell_value = executed_qty * price
                        buy_value = last_buy_qty * last_buy_price
                        profit = sell_value - buy_value
                        pct = (profit / buy_value) * 100 if buy_value > 0 else 0
                        msg = (
                            f"🔻 VENDA executada em {executed_qty:.2f} {SYMBOL} a {price:.2f} USDT (saldo total)\n"
                            f"💰 Resultado: {profit:.2f} USDT ({pct:+.2f}%)"
                        )
                        last_buy_price = None
                        last_buy_qty = None
                else:
                    msg = f"⏸️ ({SYMBOL}) Aguardar! Preço atual:  {price:.2f} USDT"
                
                print(msg)
                logging.info(msg)
                await send_message(msg)

                last_signal = signal

            await asyncio.sleep(60)  # Checa a cada 1 minuto sem bloquear o loop

        except Exception as e:
            print(f"Erro: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
