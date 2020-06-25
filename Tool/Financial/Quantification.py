import talib
import numpy

import PyBear.GlobalBear as GlobalBear

def MA(Data, TimePeriod=5):
    return talib.MA(numpy.array(Data), timeperiod=TimePeriod)

def EMA(Data, TimePeriod=5):
    return talib.EMA(numpy.array(Data), timeperiod=TimePeriod)

def BOLL(Data, TimePeriod=5):
    return talib.BBANDS(numpy.array(Data), timeperiod=TimePeriod)             

def MACD(Data, Fastperiod=12, Slowperiod=26, Signalperiod=9):
    DIF, DEA, MACD = talib.MACD(
    numpy.array(Data),
    fastperiod=Fastperiod, 
    slowperiod=Slowperiod, 
    signalperiod=Signalperiod)
    return DIF, DEA, MACD*2

def RSV(High, Low, Close):
    return talib.STOCH(
        numpy.array(High),
        numpy.array(Low),
        numpy.array(Close),
        fastk_period = 1,
        slowk_period = 1,
        slowk_matype = 0,
        slowd_period = 5,
        slowd_matype = 0,)

def RSI(Data, TimePeriod=5):
    return talib.RSI(numpy.array(Data), timeperiod=TimePeriod)

def CDLIndex(Open, High, Low, Close, Daily=True):
    Open = numpy.array(Open)
    High = numpy.array(High)
    Low = numpy.array(Low)
    Close = numpy.array(Close)
    CDLIndex  = {}

    CDLIndex['2CROWS'] = talib.CDL2CROWS(Open, High, Low, Close)
    CDLIndex['3BLACKCROWS'] = talib.CDL3BLACKCROWS(Open, High, Low, Close)
    CDLIndex['3INSIDE'] = talib.CDL3INSIDE(Open, High, Low, Close)
    CDLIndex['3LINESTRIKE'] = talib.CDL3LINESTRIKE(Open, High, Low, Close)
    CDLIndex['3OUTSIDE'] = talib.CDL3OUTSIDE(Open, High, Low, Close)
    CDLIndex['3STARSINSOUTH'] = talib.CDL3STARSINSOUTH(Open, High, Low, Close)
    CDLIndex['3WHITESOLDIERS'] = talib.CDL3WHITESOLDIERS(Open, High, Low, Close)
    CDLIndex['ABANDONEDBABY'] = talib.CDLABANDONEDBABY(Open, High, Low, Close)
    CDLIndex['ADVANCEBLOCK'] = talib.CDLADVANCEBLOCK(Open, High, Low, Close)
    CDLIndex['BELTHOLD'] = talib.CDLBELTHOLD(Open, High, Low, Close)
    CDLIndex['BREAKAWAY'] = talib.CDLBREAKAWAY(Open, High, Low, Close)
    CDLIndex['CLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(Open, High, Low, Close)
    CDLIndex['CONCEALBABYSWALL'] = talib.CDLCONCEALBABYSWALL(Open, High, Low, Close)
    CDLIndex['COUNTERATTACK'] = talib.CDLCOUNTERATTACK(Open, High, Low, Close)
    CDLIndex['DARKCLOUDCOVER'] = talib.CDLDARKCLOUDCOVER(Open, High, Low, Close)
    CDLIndex['DOJI'] = talib.CDLDOJI(Open, High, Low, Close)
    CDLIndex['DOJISTAR'] = talib.CDLDOJISTAR(Open, High, Low, Close)
    CDLIndex['DRAGONFLYDOJI'] = talib.CDLDRAGONFLYDOJI(Open, High, Low, Close)
    CDLIndex['ENGULFING'] = talib.CDLENGULFING(Open, High, Low, Close)
    CDLIndex['EVENINGDOJISTAR'] = talib.CDLEVENINGDOJISTAR(Open, High, Low, Close)
    CDLIndex['EVENINGSTAR'] = talib.CDLEVENINGSTAR(Open, High, Low, Close)
    CDLIndex['GAPSIDESIDEWHITE'] = talib.CDLGAPSIDESIDEWHITE(Open, High, Low, Close)
    CDLIndex['GRAVESTONEDOJI'] = talib.CDLGRAVESTONEDOJI(Open, High, Low, Close)
    CDLIndex['HAMMER'] = talib.CDLHAMMER(Open, High, Low, Close)
    CDLIndex['HANGINGMAN'] = talib.CDLHANGINGMAN(Open, High, Low, Close)
    CDLIndex['HARAMI'] = talib.CDLHARAMI(Open, High, Low, Close)
    CDLIndex['HARAMICROSS'] = talib.CDLHARAMICROSS(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLHIGHWAVE(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLHIKKAKE(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLHIKKAKEMOD(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLHOMINGPIGEON(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLIDENTICAL3CROWS(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLINNECK(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLINVERTEDHAMMER(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLKICKING(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLKICKINGBYLENGTH(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLLADDERBOTTOM(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLLONGLEGGEDDOJI(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLLONGLINE(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLMARUBOZU(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLMATCHINGLOW(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLMATHOLD(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLMORNINGDOJISTAR(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLMORNINGSTAR(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLONNECK(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLPIERCING(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLRICKSHAWMAN(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLRISEFALL3METHODS(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLSEPARATINGLINES(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLSHOOTINGSTAR(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLSHORTLINE(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLSPINNINGTOP(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLSTALLEDPATTERN(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLSTICKSANDWICH(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLTAKURI(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLTASUKIGAP(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLTHRUSTING(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLTRISTAR(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLUNIQUE3RIVER(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLUPSIDEGAP2CROWS(Open, High, Low, Close)
    CDLIndex['2CROWS'] = talib.CDLXSIDEGAP3METHODS(Open, High, Low, Close)

    if Daily:
        Ret = []
        for Counter in range(len(CDLIndex[0])):
            APList = []
            for Item in list(CDLIndex):
                if Item[Counter] == 0:
                    APList.append(0)
                else:
                    APList.append(1)
            Ret.append(APList)
        return Ret
    else:
        for Item in CDLIndex:
            for Counter in range(len(Item)):
                if Item[Counter] == 100:
                    Item[Counter] = 1
                elif Item[Counter] == -100:
                    Item[Counter] = 2
        return CDLIndex