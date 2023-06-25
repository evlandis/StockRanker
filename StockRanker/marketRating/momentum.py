import pandas as pd
import yfinance as yf

import matplotlib.dates as mpl_dates

from datetime import datetime
from dateutil.relativedelta import *
    






# get stock prices using yfinance library
def get_current_average_over_historic(symbol,dfString,totalMonthsBack,currentDaysBack,until):
    currentDate = datetime.now()
    startDate = currentDate +relativedelta(months=-(totalMonthsBack+1))
    #print(startDate)
    df = yf.download(symbol, start=startDate, threads= False)
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close','Volume']]
    #total days from startdate to current date
    totalDays = df.shape[0]
    #day the average changes from previous average to current average


    #get historical average
    #print(totalDays)
    total = 0
    daysI = 0
    for i in range(totalDays - (totalMonthsBack*30), totalDays - until):
        daysI+=1
        total+=float(df[dfString][i])
    numberOfDays = (totalMonthsBack*30)-until
    print(numberOfDays,daysI)
    avg = total/numberOfDays

    #get current average
    currTotal = 0
    daysJ=0
    for j in range(totalDays - currentDaysBack, totalDays - until):
        daysJ+=1
        currTotal+=float(df[dfString][j])
    numberOfDays = currentDaysBack - until
    print(numberOfDays,daysJ)
    currAvg = currTotal/numberOfDays

    #get multiplier
    currentAvgOverHistoricAvg = currAvg/avg
    print(currAvg,avg)


    #print(symbol,avg,currAvg,currentAvgOverHistoricAvg)
    return currentAvgOverHistoricAvg






#use this when importing
def get_momentum(ticker,totalMonthsBack=6,currentDaysBack=30,until=1):
    volumeMomentum = get_current_average_over_historic(ticker,"Volume",totalMonthsBack,currentDaysBack,until)
    priceMomentum = get_current_average_over_historic(ticker,"Close",totalMonthsBack,currentDaysBack,until)
    volumeDirection = volumeMomentum - 1
    priceDirection = priceMomentum - 1
    #EDGE CASE: ensures if both directions are negative, the current momentum is negative
    if volumeDirection<0 and priceDirection<0:
        currentMomentum = -volumeDirection/priceDirection
    #if only 1 or none is negative, it will work as is
    else:
        currentMomentum = volumeDirection/priceDirection
        print(volumeDirection,priceDirection)
    return currentMomentum

print(get_momentum("XLK",2,10,1))