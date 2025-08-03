from src.utils.indicators import moving_averages

#Verifica sinal de compra ou venda baseado no cruzamento de médias móveis
def check_signal(df):
    if len(df) < 40: # Precisa ter pelo menos 40 candles
        return "hold"
    
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Cruzamento para COMPRA
    if prev['ma_fast'] <= prev['ma_slow'] and last['ma_fast'] > last['ma_slow']:
        return "BUY"

    # Cruzamento para VENDA
    if prev['ma_fast'] >= prev['ma_slow'] and last['ma_fast'] < last['ma_slow']:
        return "SELL"

    return "hold"
