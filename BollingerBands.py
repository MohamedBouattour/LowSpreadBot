import time
from binance import Client
from binance.enums import ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
import pandas as pd

from exchanger import getBianceClient, getTaapiSecret


client = getBianceClient()
qty = 20
rio = 1
import requests


def getMinuteData(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(
        symbol, interval, lookback))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    return frame


def strategy(symbol, qty=qty, entried=False, rio = 1):
    bbData = requests.get("https://api.taapi.io/bbands2?secret="+getTaapiSecret()+"&exchange=binance&symbol=XRP/USDT&interval=15m&stddev=1")
    if rio >= 1.1:
        qty = qty + 1
        rio = 1
    df = getMinuteData(symbol, '5m', '15 minute ago UTC')
    if not entried:
        entryPrice = float(client.get_avg_price(symbol = symbol)['price'])
        if float(df.Close[-1]) > float(bbData.json()['valueUpperBand']):
            Client.create_order(self=client, symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=qty)
            print('Buy@'+str(entryPrice))
            Client.create_order(self=client, symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_LIMIT, quantity=qty,   timeInForce=TIME_IN_FORCE_GTC, price=format(float(entryPrice*1.004),'.4f'))
        elif float(df.Close[-1]) < float(bbData.json()['valueLowerBand']):
            print('Sell@'+str(entryPrice))
            Client.create_order(self=client, symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_LIMIT, quantity=qty,   timeInForce=TIME_IN_FORCE_GTC,price=format(float(entryPrice*1.996),'.4f'))
        else:
            print('No trade has been executed')
            time.sleep(30)
            strategy('XRPUSDT', qty, entried=False, rio = rio)
    if entried:
        while True:
            print(rio)
            time.sleep(420)
            orders = client.get_open_orders(symbol='XRPUSDT')
            print(rio)
            if len(orders) == 0:
                entried = False
                rio = rio*1.004
                strategy('XRPUSDT', qty, entried=False)
            


balance = client.get_asset_balance(asset = 'USDT')
if float(balance['free']) > 20:
    hasOrders = False
else:
    hasOrders = True
strategy('XRPUSDT', qty, entried=hasOrders, rio = 1)
