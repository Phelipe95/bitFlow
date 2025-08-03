from binance.client import Client
from config.settings import API_KEY, API_SECRET, SYMBOL
import pandas as pd
import math

client = Client(API_KEY, API_SECRET)

# Busca candles (klines) da Binance e retorna em DataFrame
def get_klines(symbol, interval="15m", limit=100):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

        data = []
        for k in klines:
            data.append({
                "time": pd.to_datetime(k[0], unit="ms"), # converte timestamp
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5])
            })

        df = pd.DataFrame(data)
        df.set_index("time", inplace=True) # tempo com índice
        return df
    
    except Exception as e:
        print(f"❌ Erro ao buscar klines: {e}")
        return pd.DataFrame()

# Teste de conexão simples    
def test_connection():
    try:
        client.ping()
        print("✅ Conectado à Binance com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar na Binance: {e}")
        return False
    
# Testa se as credenciais da conta estão válidas
def test_account():
    try:
        account = client.get_account()
        usdt_balance = next(b["free"] for b in account["balances"] if b["asset"] == "USDT")
        print(f"✅ Conexão autenticada! Conta encontrada.")
        print(f"Saldo disponível em USDT: {usdt_balance}")
        return True
    except Exception as e:
        print(f"❌ Erro na autenticação com a Binance: {e}")
        return False

# Executar ordens com limite de $10
def place_order(symbol, side, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        print(f"✅ Ordem executada: {side} {quantity} {symbol}")
        return order
    except Exception as e:
        print(f"❌ Erro ao executar ordem {e}")
        return None
    
def buy_solana(symbol=SYMBOL, max_usdt=10):
    balance = float(next(b["free"] for b in client.get_account()["balances"] if b["asset"] == "USDT"))

    if balance <= 0:
        print("❌ Saldo insuficiente em USDT para comprar.")
        return None
    
    usdt_to_spend = min(balance, max_usdt)

    # Preço atual da SOL
    price = float(client.get_symbol_ticker(symbol=symbol)["price"])
    qty = usdt_to_spend / price

    # Binance geralmente exige 2 casas decimais na quantidade de SOL
    qty = round(qty, 2)

    return place_order(symbol, "BUY", qty)

def sell_solana(symbol=SYMBOL):
    balance = float(next(b["free"] for b in client.get_account()["balances"] if b["asset"] == "SOL"))

    if balance <= 0:
        print("❌ Saldo insuficiente em SOL para vender.")
        return None
    
    qty = round(balance, 2) # ajusta casa decimais

    return place_order(symbol, "SELL", qty)