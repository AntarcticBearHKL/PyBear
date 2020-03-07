import os,sys
import tushare
import talib
import numpy
import pandas
import warnings
warnings.filterwarnings('ignore')

from PyBear.GlobalBear import *
from PyBear.Library.Multitasks import *
from PyBear.Library.Time import *
from PyBear.Library.RegularExpression import *
from PyBear.Library.Data.File import *
from PyBear.Library.Data.TimeSequence import *
from PyBear.Library.Data.LogicSequence import *
from PyBear.Library.Statistics import *

TushareAvailiable = False
def SetTushareToken(token):
    tushare.set_token('85eca8e96158d3127814bcde6bf4c000326799ae66b54030d51ccde5')
    TushareAvailiable = True

class CHN:
    class MacroMarket:
        def __init__(self):
            pass

    class BondMarket:
        def __init__(self):
            pass

    class StockMarket:
        def __init__(self, tradeday='updated'):
            if not TushareAvailiable:
                raise BadBear('Tushare Cannot Use Without Token')
            self.baseName = None
            self.api = tushare.pro_api()

        def updateInfo(self):
            print('updateInfo')
            ts_data = self.api.stock_basic()
            print(ts_data)
            for item in range(len(ts_data)):
                stock = LogicSequence(self.baseName, ts_data.loc[item]['ts_code'])
                stock.defineProperty('name', ts_data.loc[item]['area'])
                stock.defineProperty('area', ts_data.loc[item]['name'])
                stock.defineProperty('industry', ts_data.loc[item]['industry'])
                stock.defineProperty('market', ts_data.loc[item]['market'])
                stock.defineProperty('startDate', ts_data.loc[item]['list_date'])
                LogicSequence(self.baseName, 'AllStockCode').defineHave(ts_data.loc[item]['ts_code'])


        def updateTradeDay(self, latest=False):
            tradeday = self.api.trade_cal(exchange='', start_date='20000101', end_date='20181231')
            print(tradeday)
            ret = {}
            for item in range(len(tradeday)):
                ret[tradeday.loc[item]['cal_date']] = str(tradeday.loc[item]['is_open'])
            TimeSequence(self.baseName, 'TradeDay').feed(ret)

        def getStockCodeList(self):
            return LogicSequence(self.baseName, 'AllStockCode')['have']

    class FutureMarket:
        def __init__(self):
            pass

    class OptionMarket:
        def __init__(self):
            pass

    class FundMarket:
        def __init__(self):
            pass

    
    class Bond:
        def __init__(self):
            pass

    class Stock:
        def __init__(self, code):
            self.stockMarket = CHN.StockMarket()
            self.baseName = Config.CNHStockHome
            self.code = code
              
        def fulldownload(self):
            tick = tushare.pro_bar(ts_code = self.code, adj='qfq', start_date='20010101', end_date=Date().to_string(style='S1'))
            
            _open = {}
            _close = {}
            _high = {}
            _low = {}
            _vol = {}
            for item in range(len(tick)):
                _open[tick.loc[item]['trade_date']] = tick.loc[item]['open']
                _close[tick.loc[item]['trade_date']] = tick.loc[item]['close']
                _high[tick.loc[item]['trade_date']] = tick.loc[item]['high']
                _low[tick.loc[item]['trade_date']] = tick.loc[item]['low']
                _vol[tick.loc[item]['trade_date']] = tick.loc[item]['vol']
            TimeSequence(self.baseName, self.code + '_open').feed(_open)
            TimeSequence(self.baseName, self.code + '_close').feed(_close)
            TimeSequence(self.baseName, self.code + '_high').feed(_high)
            TimeSequence(self.baseName, self.code + '_low').feed(_low)
            TimeSequence(self.baseName, self.code + '_vol').feed(_vol)
            print(Date() - t)
            t = Date()
            print('Finish Download Tick: ' + self.code)

        def update(self):
            pass

        def updated(self):
            pass

        def getOpen(self):
            pass

        def getClose(self):
            pass

        def getHigh(self):
            pass

        def getLow(self):
            pass

     
    class Future:
        def __init__(self):
            pass

    class Option:
        def __init__(self):
            pass

    class Fund:
        def __init__(self):
            pass


class GLOBAL:
    class CurrencyMarket:
        def __init__(self):
            pass

    class DigitalCurrencyMarket:
        def __init__(self):
            pass


    class Currency:
        def __init__(self):
            pass

    class DigitalCurrency:
        def __init__(self):
            pass


class Quantification:
    def __init__(self, code):
        self.stockInfo = StockInfo(code)

    def RSV(self, days=120, range=5):
        rsv = talib.STOCH(numpy.array(self.stockInfo.getHigh(days=days)),
        numpy.array(self.stockInfo.getLow(days=days)),
        numpy.array(self.stockInfo.getClose(days=days)),
        fastk_period = range,
        slowk_period = 1,
        slowk_matype = 0,
        slowd_period = 5,
        slowd_matype = 0,)[0]
        return rsv

    def RSI(self, days=120, range=5):
        rsi = talib.RSI(numpy.array(self.stockInfo.getOpen(days=days)), 5)
        return rsi

    def MA(self, days=120, range=5):
        ma = talib.MA(numpy.array(self.stockInfo.getOpen(days=days)), timeperiod=range) 
        return ma

    def EMA(self, days=120, range=5):
        ema = talib.EMA(numpy.array(self.stockInfo.getOpen(days=days)), timeperiod=range) 
        return ema

    def BOLL(self, days=120, range=5):
        pass

    def MACD(self, days=120, fastperiod=5, slowperiod=20, signalperiod=9):
        dif, dea, macd = talib.MACD(
        numpy.array(self.stockInfo.getOpen(days=days)),
        fastperiod=fastperiod, 
        slowperiod=slowperiod, 
        signalperiod=signalperiod) 
        return [dif, dea, macd*2]


class Brokor:
    def __init__(self):
        pass


class Analyst:
    def __init__(self):
        pass

    def do(market, fn, core, thread):
        TP = ThreadMatix(core, thread)
        meglist = TP.getList()

        TP.newAutoTasks(
            market, 
            fn,
            [meglist] 
            )
        TP.start()

        print(meglist)
        print(len(meglist))

if GlobalAvailabilityCheck:
    pass