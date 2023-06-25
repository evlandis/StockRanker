#  #Library
# from tracemalloc import start
# import yfinance as yf
from datetime import datetime
import re
from dateutil.relativedelta import *
# from tipranks.tipranksAttempt import AveragePriceTarget
    
#  #Load Stock price

from yahoo_fin.stock_info import get_data

# import necessary libraries for finding support and resistance levels using yahoo finance
import pandas as pd
import yfinance as yf
import numpy as np
import math
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

# import for tipranks price targets
import repackage
repackage.up()
from tipranks.tipranks import base
#

from mimetypes import init
from tipranks import TipRanks
tr = TipRanks(
    email="evlandis2587@gmail.com",
    password="@Qwerty123"
)




def AveragePriceTarget(currTicker):
    ls = tr.anaylst_projection(ticker=currTicker)
    length = 0
    totalPrice = 0
    for elem in ls:
        ratingsList = elem["ratings"]
        for ratings in ratingsList:
            priceTarget = ratings["priceTarget"]
            if type(priceTarget)==float:
                length+=1
                totalPrice+=priceTarget
        

    averagePrice = totalPrice/max(length,1)
    print(currTicker,averagePrice)
    return averagePrice


date = datetime.now()
startDate = date +relativedelta(months=-12)



# get stock prices using yfinance library
def get_stock_price(symbol):
  df = yf.download(symbol, start=startDate, threads= False)
  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
  return df
# symbol = 'DDOG'
# df = get_stock_price(symbol)

print(get_stock_price("MSFT"))
#method 1: fractal candlestick pattern
# determine bullish fractal 
def is_support(df,i):  
  cond1 = df['Low'][i] < df['Low'][i-1]   
  cond2 = df['Low'][i] < df['Low'][i+1]   
  cond3 = df['Low'][i+1] < df['Low'][i+2]   
  cond4 = df['Low'][i-1] < df['Low'][i-2]  
  return (cond1 and cond2 and cond3 and cond4) 
# determine bearish fractal
def is_resistance(df,i):  
  cond1 = df['High'][i] > df['High'][i-1]   
  cond2 = df['High'][i] > df['High'][i+1]   
  cond3 = df['High'][i+1] > df['High'][i+2]   
  cond4 = df['High'][i-1] > df['High'][i-2]  
  return (cond1 and cond2 and cond3 and cond4)
# to make sure the new level area does not exist already
def is_far_from_level(value, levels, df):    
  ave =  np.mean(df['High'] - df['Low'])    
  return np.sum([abs(value-level)<ave for _,level in levels])==0
# a list to store resistance and support levels


def findSupportAndResistanceForStock(df):
    supports, resistance = [], []
    lowestSupport = float("inf")

    currSupport = float("inf")
    
    for i in range(2, df.shape[0] - 2):  
        if is_support(df, i):    
            low = df['Low'][i]    
            if is_far_from_level(low, supports, df):      
                supports.append((i, low)) 
                lowestSupport = min(lowestSupport,low) 
                currSupport = low

    if currSupport!=float("inf"):
      return [lowestSupport,currSupport]



def calculateRiskToRewardRatio(ticker,currentPrice,supportAndResistanceList):
  risk = float(supportAndResistanceList[0])
  reward = AveragePriceTarget(ticker)
  if reward:
    Ratio = abs(((reward/currentPrice)-1)/((risk/currentPrice)-1))
    print(ticker,Ratio,"Average Projection: ",reward,"Current Price",currentPrice, "Support: ",risk)
    return Ratio



def findSupportAndResistanceForStockList(ticker):
    df = get_stock_price(ticker)
    if not df.empty:
        supportAndResistance = findSupportAndResistanceForStock(df)
        if supportAndResistance:
            currentPrice = df['Close'][-1]
            Ratio = calculateRiskToRewardRatio(ticker,currentPrice,supportAndResistance)
        if Ratio:
            return Ratio
        else:
            print("unable to be found")
            return 0     


calculateRiskToRewardRatio("MSFT")