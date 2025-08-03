import pandas as pd

#Calcula médias móveis de curto e longo prazo
def moving_averages(data, short=7, long=40): 
    df = pd.DataFrame(data)
    df['ma_fast'] = df['close'].rolling(window=short).mean()
    df['ma_slow'] = df['close'].rolling(window=long).mean()
    return df
