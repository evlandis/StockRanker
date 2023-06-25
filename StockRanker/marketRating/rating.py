
from momentum import get_momentum
from meanReversion import calculateRiskToRewardRatio


economiesList = ["SPY","VWO","XLK","XLF","XLRE","XLE","XLY","XLI","XLV","XLP"]

def compareEconomies(economiesList):
    rank = []
    for ticker in economiesList:
        try:
            momentum = get_momentum(ticker,12,70,50)
            meanReversion = calculateRiskToRewardRatio(ticker)
            rank.append([ticker,momentum,meanReversion,momentum+meanReversion])

        except:
            pass
        for i in rank:
            print(i)



    

compareEconomies(economiesList)





