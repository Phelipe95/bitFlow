from src.utils.indicators import moving_averages

#Verifica sinal de compra ou venda baseado no cruzamento de médias móveis
def check_signal(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Cruzamento para COMPRA
    if prev['MA_Short'] <= prev['MA_Long'] and last['MA_Short'] > last['MA_Long']:
        return "BUY"

    # Cruzamento para VENDA
    if prev['MA_Short'] >= prev['MA_Long'] and last['MA_Short'] < last['MA_Long']:
        return "SELL"

    return None
