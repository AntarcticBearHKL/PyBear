import os,sys
import tushare
import talib
import numpy
import pandas
import warnings
warnings.filterwarnings('ignore')

from PyBear.GlobalBear import *
from PyBear.Library.Multitasks import *
from PyBear.Library.Chronus import *
from PyBear.Library.Data.File import *
from PyBear.Library.Statistics import *
from PyBear.Library.Data.MySQL import *

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
        def __init__(self, ServerName, UserName):
            if TushareAvailiable:
                raise BadBear('Tushare Cannot Use Without Token')
            self.BaseName = None
            self.API = tushare.pro_api()

            self.BasicInfoTable = DatabaseTable(ServerName, UserName, 'StockMarket', 'BasicInfo')
            self.BasicInfoTable.CheckColumn({
                'Code': 'CHAR(10) NOT NULL',
                'Name': 'CHAR(12) NOT NULL',
                'Area': 'CHAR(6) NOT NULL',
                'Industry': 'CHAR(12) NOT NULL',
            }, Index=['Code'])

            print(self.BasicInfoTable.SearchTable('ID', 3794))

            self.TradeDayTable = DatabaseTable(ServerName, UserName, 'StockMarket', 'TradeDay')

        def UpdateBasicInfo(self):
            BasicInfo = self.API.stock_basic()
            Values = []
            for Item in BasicInfo.itertuples():
                Values.append([Item.symbol, Item.name, Item.area, Item.industry])
            self.BasicInfoTable.DeleteAll()
            self.BasicInfoTable.Insert(['Code', 'Name', 'Area', 'Industry'], Values)

        def UpdateTradeDay(self, latest=False):
            tradeday = self.API.trade_cal(exchange='', start_date='20000101', end_date='20181231')
            print(tradeday)
            ret = {}
            for item in range(len(tradeday)):
                ret[tradeday.loc[item]['cal_date']] = str(tradeday.loc[item]['is_open'])
            TimeSequence(self.BaseName, 'TradeDay').feed(ret)

        def GetStockCodeList(self):
            return LogicSequence(self.BaseName, 'AllStockCode')['have']

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
            self.BaseName = Config.CNHStockHome
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
            TimeSequence(self.BaseName, self.code + '_open').feed(_open)
            TimeSequence(self.BaseName, self.code + '_close').feed(_close)
            TimeSequence(self.BaseName, self.code + '_high').feed(_high)
            TimeSequence(self.BaseName, self.code + '_low').feed(_low)
            TimeSequence(self.BaseName, self.code + '_vol').feed(_vol)
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