import pandas as pd
import yfinance as yf
import numpy as np
import math
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

from datetime import datetime
import re
from dateutil.relativedelta import *
    


date = datetime.now()
startDate = date +relativedelta(months=-36)


# get stock prices using yfinance library
def get_stock_price(symbol):
    df = yf.download(symbol, start=startDate, threads= False)
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close','Volume']]
    total_price = 0
    daysI = 0
    for i in range(df.shape[0] - 30, df.shape[0] - 2):
        daysI+=1
        total_price+=float(df['Close'][i])
    avg_price = total_price/daysI

    currTotal_price = 0
    daysJ = 0
    for j in range(df.shape[0]-9,df.shape[0] - 2):
        daysJ+=1
        currTotal_price+=float(df['Close'][j])
    currAvg_price = currTotal_price/daysJ

    currentPriceOverHistoricPrice = currAvg_price/avg_price

    print(symbol,avg_price,currAvg_price,currentPriceOverHistoricPrice)

get_stock_price("IRBO")