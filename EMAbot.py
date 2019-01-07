#!/usr/bin/python3
import calendar
import ccxt
from datetime import datetime
import json
import numpy as np
import pandas as pd 
import requests
import time
def get_price(min,n):
   try:
       now = datetime.utcnow()
       unixtime = calendar.timegm(now.utctimetuple())
       since = unixtime - 60 * 60
       query = {"period": str(min),"after": str(since),"before": str(unixtime)}
       data = json.loads(requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc",params=query).text)
       return { "close_time" : data["result"][str(min)][n][0],
               "close_price": data["result"][str(min)][n][4]},data
   except Exception as e:
       print(e.args)
       time.sleep(10)
def create_position(side):
   try:
       order = bitflyer.create_order(
           symbol = 'BTC/JPY',
           type='market',
           side= side,
           amount='0.1',
           params = { "product_code" : "FX_BTC_JPY" })
       print("成行注文しました!!")
       flag["order"] = True
       flag["position"] = side
       time.sleep(10)
       return flag
   except:
       print("成行注文に失敗しました(;_;)")
def close_position(side):
   while True:
       try:
           order = bitflyer.create_order(
				symbol = 'BTC/JPY',
				type='market',
				side= side,
				amount='0.1',
				params = { "product_code" : "FX_BTC_JPY" })
           print("成行決済しました!!")
           flag["order"] = False
           flag["position"] = 0
           time.sleep(10)
           return flag
       except:
           print("成行決済に失敗しました(;_;)")
           time.sleep(10)
def EMA(EMA_period,period):
   for n in [str(period)]:
       row = full_data["result"][str(period)]
       df = pd.DataFrame(row,
                       columns=['exectime', 
                               'open', 
                               'high', 
                               'low', 
                               'close', 
                               'price', 
                               'volume'])
   alpha = 2/(EMA_period+1)
   ema = df['close'].ewm(alpha=alpha).mean()[-1:]
   return int(ema.values[0])
def check_order(EMA_period,period):
   if flag["order"] == True:
       if flag["position"] == 'buy':
           if EMA(EMA_period,period) < data["close_price"] and EMA(EMA_period,period) > tmp["close_price"]:
               close_position("sell")
       elif flag["position"] == 'sell':
           if EMA(EMA_period,period) > data["close_price"] and EMA(EMA_period,period) < tmp["close_price"]:
               close_position("buy")
   else:
       if EMA(EMA_period,period) < data["close_price"] and EMA(EMA_period,period) > tmp["close_price"]:
           create_position("buy")
       elif EMA(EMA_period,period) > data["close_price"] and EMA(EMA_period,period) < tmp["close_price"]:
           create_position("sell")

#=====================================================#
bitflyer = ccxt.bitflyer({
   'apiKey':'あなたのapikey',
   'secret':'あなたのsecret'
})
tmp,unuse = get_price(60,-2)
flag = {
   'order':False,
   'position': 0
}
time.sleep(30)
while True:
   data,full_data = get_price(60,-2)
   if data["close_time"] != tmp["close_time"]:
       check_order(14,60)
       tmp["close_price"] = data["close_price"]
       tmp["close_time"] = data["close_time"]
   time.sleep(10)
