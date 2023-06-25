import pandas as pd
import yfinance as yf

import matplotlib.dates as mpl_dates

from datetime import datetime
from dateutil.relativedelta import *
    


currentDate = datetime.now()
startDate = currentDate +relativedelta(months=-2)


# get stock prices using yfinance library
def get_current_average_over_historic(symbol,dfString):
    df = yf.download(symbol, start=startDate, threads= False)
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close','Volume']]
    #total days from startdate to current date
    totalDays = df.shape[0]
    #day the average changes from previous average to current average
    dayChange = 5

    #get historical average
    total = 0
    for i in range(totalDays - 30, totalDays - dayChange):
        total+=float(df[dfString][i])
    numberOfDays = 30-dayChange
    avg = total/numberOfDays

    #get current average
    currTotal = 0
    for j in range(totalDays - dayChange, totalDays - 1):
        currTotal+=float(df[dfString][j])
    numberOfDays = dayChange - 1
    currAvg = currTotal/numberOfDays

    #get multiplier
    currentAvgOverHistoricAvg = currAvg/avg


    print(symbol,avg,currAvg,currentAvgOverHistoricAvg)
    return currentAvgOverHistoricAvg






#use this when importing
def get_momentum(ticker,volumeString,priceString):
    volumeMomentum = get_current_average_over_historic(ticker,volumeString)
    priceMomentum = get_current_average_over_historic(ticker,priceString)
    volumeDirection = volumeMomentum - 1
    priceDirection = priceMomentum - 1
    #EDGE CASE: ensures if both directions are negative, the current momentum is negative
    if volumeDirection<0 and priceDirection<0:
        currentMomentum = -volumeDirection/priceDirection
    #if only 1 or none is negative, it will work as is
    else:
        currentMomentum = volumeDirection/priceDirection
    print(currentMomentum)

