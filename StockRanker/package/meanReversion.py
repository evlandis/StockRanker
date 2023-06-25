#  #Library
# from tracemalloc import start
# import yfinance as yf
from datetime import datetime
import re
from dateutil.relativedelta import *
# from tipranks.tipranksAttempt import AveragePriceTarget
    
#  #Load Stock price



# import for tipranks price targets



#

from yahoo_fin.stock_info import get_data

# import necessary libraries for finding support and resistance levels using yahoo finance
import pandas as pd
import yfinance as yf
import numpy as np
import math
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt


date = datetime.now()
startDate = date +relativedelta(months=-36)



# get stock prices using yfinance library
def get_stock_price(symbol):
  df = yf.download(symbol, start=startDate, threads= False)
  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
  return df
# symbol = 'DDOG'
# df = get_stock_price(symbol)

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
    highestResistance = 0
    currSupport = float("inf")
    print(df.shape[0])
    for i in range(2, df.shape[0] - 2):  
        if is_support(df, i):    
            low = df['Low'][i]    
            if is_far_from_level(low, supports, df):      
                supports.append((i, low)) 
                lowestSupport = min(lowestSupport,low) 
                currSupport = low
        elif is_resistance(df, i):    
            high = df['High'][i]
            print(high)
            if is_far_from_level(high, resistance, df):      
                resistance.append((i, high))
                print(highestResistance,high)
                highestResistance = max(highestResistance, high)
                
    if currSupport!=float("inf") and highestResistance:
      return [lowestSupport,currSupport,highestResistance]

def findAllTimeHigh(df):
  maxHigh = 0
  for i in range(2,df.shape[0]-2):
    currHigh = df['High'][i]
    maxHigh = max(maxHigh, currHigh)
  return maxHigh


def calculateRiskToRewardRatio(ticker):
  df = get_stock_price(ticker)
  supportAndResistanceList = findSupportAndResistanceForStock(df)
  risk = float(supportAndResistanceList[0])
  reward = float(supportAndResistanceList[2])
  currentPrice = df['Close'][-1]
  if reward:
    Ratio = abs(((reward/currentPrice)-1)/((risk/currentPrice)-1))
    return (ticker,Ratio,"3 Year High: ",reward,"Current Price",currentPrice, "Support: ",risk)

print(calculateRiskToRewardRatio("WCLD"))
    