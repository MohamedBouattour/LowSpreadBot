from utils import getMinuteData ,getBianceClient
import pandas_ta as ta


symbols = ['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','ADAUSDT','XRPUSDT','DOTUSDT','AVAXUSDT','LUNAUSDT','MATICUSDT','LINKUSDT','ALGOUSDT','MANAUSDT','EGLDUSDT','XLMUSDT','VETUSDT','TRXUSDT','FILUSDT','SANDUSDT','ENJUSDT','RUNEUSDT','XECUSDT','CHZUSDT','KSMUSDT','BATUSDT','BTTUSDT','TFUELUSDT','IOTXUSDT']
print(len(symbols))
for symbol in symbols:
    df = getMinuteData(symbol, '2h', '15 day ago UTC')
    for index, row in df.iterrows():
        row['Close'] = float(row['Close'])
        row['Open'] = float(row['Open'])
    df.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)
    df.ta.rsi(length=14, append=True)
    df.index = range(1, len(df)+1)
    result = []
    if(float(df.iloc[-1]['RSI_14'])<30):
        #print(symbol,': ',df.iloc[-1]['RSI_14'])
        result.append(symbol)
if len(result) == 0:
    print('no good opportunity to buy')
else:
    print(result)

    