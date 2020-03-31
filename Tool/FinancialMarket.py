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
            self.API = tushare.pro_api()
            self.ServerName = ServerName
            self.UserName = UserName
            self.UpdateManager = None

            self.BasicInfoTable = DatabaseTable(ServerName, UserName, 'CHNStockMarket', 'BasicInfo', Reload=False)
            self.TradeDayTable = DatabaseTable(ServerName, UserName, 'CHNStockMarket', 'TradeDay')

        def UpdateBasicInfo(self):
            self.BasicInfoTable.CheckColumn({
                'CodeIDX': 'BIGINT NOT NULL',
                'Code': 'CHAR(16) NOT NULL',
                'Name': 'CHAR(16) NOT NULL',
                'Area': 'CHAR(8) NOT NULL',
                'Industry': 'CHAR(16) NOT NULL',
            }, Index=['CodeIDX'])

            self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo',))

            BasicInfo = self.API.stock_basic()

            Values = []
            for Item in BasicInfo.itertuples():
                Values.append([int(Item.symbol), Item.symbol, Item.name, Item.area, Item.industry])
            
            self.BasicInfoTable.DeleteAll()
            self.BasicInfoTable.Insert(['CodeIDX', 'Code', 'Name', 'Area', 'Industry'], Values)

            self.UpdateManager.Update('BasicInfo')


        def UpdateTradeDay(self, latest=False):
            self.TradeDayTable.CheckColumn({
                'Date': 'INT NOT NULL',
                'Open': 'INT NOT NULL',
            }, Index=['Date'])

            self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo', Reload=False)) 

            TradeDay = self.API.trade_cal(exchange='', start_date='20000101', end_date='20181231')

            Values = []
            for Item in TradeDay.itertuples():
                Values.append([int(Item.cal_date), int(Item.is_open)])
            
            self.TradeDayTable.DeleteAll()
            self.TradeDayTable.Insert(['Date', 'Open'], Values)

            self.UpdateManager.Update('TradeDay')

        def SZStock(self):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            if not self.UpdateManager.TableUpdateTime('BasicInfo'):
                self.UpdateBasicInfo()
            return [Item[2]+'.SZ' for Item in self.BasicInfoTable.SearchTable('WHERE CodeIDX<300000')]

        def ZXStock(self):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            if not self.UpdateManager.TableUpdateTime('BasicInfo'):
                self.UpdateBasicInfo()
            return [Item[2]+'.SZ' for Item in self.BasicInfoTable.SearchTable('WHERE CodeIDX<600000 AND CodeIDX>300000')]

        def SHStock(self):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            if not self.UpdateManager.TableUpdateTime('BasicInfo'):
                self.UpdateBasicInfo()
            return [Item[2]+'.SH' for Item in self.BasicInfoTable.SearchTable('WHERE CodeIDX<680000 AND CodeIDX>600000')]
        def KCStock(self):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            if not self.UpdateManager.TableUpdateTime('BasicInfo'):
                self.UpdateBasicInfo()
            return [Item[2]+'.SH' for Item in self.BasicInfoTable.SearchTable('WHERE CodeIDX>680000')]

    class FundMarket:
        def __init__(self):
            pass

    class CommodityMarket:
        def __init__(self):
            pass

    class RealEstateMarket:
        def __init__(self):
            pass

    
    class Bond:
        def __init__(self):
            pass

    class Stock:
        def __init__(self, ServerName, UserName, Code):
            self.StockMarket = None
            self.Code = Code
            self.ServerName = ServerName
            self.UserName = UserName
            self.UpdateManager = None
            
            self.TickTable = DatabaseTable(ServerName, UserName, 'CHNStockMarket', self.Code[:6]+'_Price', Reload=False)
              
        def FullDownload(self):
            self.TickTable.CheckColumn({
                'Date':             'INT NOT NULL',
                'Open':             'DECIMAL(6,4) NOT NULL',
                'High':             'DECIMAL(6,4) NOT NULL',
                'Low':              'DECIMAL(6,4) NOT NULL',
                'Close':            'DECIMAL(6,4) NOT NULL',
                'ChangedPrice':     'DECIMAL(6,4) NOT NULL',
                'ChangedPercent':   'DECIMAL(6,4) NOT NULL',
                'Volume':           'DECIMAL(13,4) NOT NULL',
                'Amount':           'DECIMAL(13,4) NOT NULL',
            }, Index=['Date'])
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 

            Tick = tushare.pro_bar(ts_code = self.Code, adj='qfq', start_date='20050101', end_date=Date().String(Style='SS'))

            Values = []
            for Item in Tick.itertuples():
                Values.append([
                    int(Item.trade_date),
                    float(Item.open),
                    float(Item.high),
                    float(Item.low),
                    float(Item.close),
                    float(Item.change),
                    float(Item.pct_chg),
                    float(Item.vol),
                    float(Item.amount),
                    ])
            Values.reverse()
            
            self.TickTable.DeleteAll()
            self.TickTable.Insert(['Date', 'Open', 'High', 'Low', 'Close', 'ChangedPrice', 'ChangedPercent', 'Volume', 'Amount'], Values)

            self.UpdateManager.Update(self.Code[:6]+'_Price')
            print(self.Code+' Full Download Finished')
            
        def Update(self):
            pass

        def Sync(self):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            Exist = self.UpdateManager.TableUpdateTime(self.Code+'_Price')

            if not Exist:
                self.FullDownload() 
                return

            if not self.StockMarket:
                self.StockMarket = CHN.StockMarket(self.ServerName, self.UserName)
            self.StockMarket

            Date().String()

        def getOpen(self):
            pass

        def getClose(self):
            pass

        def getHigh(self):
            pass

        def getLow(self):
            pass

    class Fund:
        def __init__(self):
            pass
     
    class Commodity:
        def __init__(self):
            pass

    class RealEstate:
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