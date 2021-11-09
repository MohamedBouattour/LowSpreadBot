from binance.enums import ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
from binance import Client
from utils import getMinuteData
from exchanger import getBianceClient

amount = 15
symbol ='ADAUSDT'

entred = False
buys = []
sells = []
client = getBianceClient()
def strat(symbol,amount,entred):
    df = getMinuteData(symbol, '1h', '15 hour ago UTC')
    for index, row in df.iterrows():
        row['Close'] = float(row['Close'])
        row['Open'] = float(row['Open'])
    df.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)
    df.ta.rsi(length=14, append=True)
    pd.set_option("display.max_columns", None)
    df.index = range(1, len(df)+1)
    if not entred:
        if float(df.iloc[-1]['RSI_14']):
            order = Client.create_order(self=client, symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=amount)
            target = format(float(order['fills'][0]['price']) * 1.02, '.4f')
            Client.create_order(self=client, symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_LIMIT, quantity=amount,timeInForce=TIME_IN_FORCE_GTC, price=target)
            entred = True
        else:
            print('no Trade rsi = '+str(df.iloc[-1]['RSI_14']))
            time.sleep(1800)
            strat(symbol, amount, entred)
    elif entred:
        while True:
            orders = client.get_open_orders(symbol=symbol)
            if len(orders) == 0:
                entred = False
                strat(symbol, amount*1.02, entred)
            

orders = client.get_open_orders(symbol='XRPBTC')
if len(orders) == 0:
    hasOrders = False
else:
    hasOrders = True
strat(symbol, amount, entried=hasOrders, rio = 1)