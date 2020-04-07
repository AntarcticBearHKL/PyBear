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

            self.DB = Database(ServerName, UserName, 'CHNStockMarket')
            self.BasicInfoTable = DatabaseTable(ServerName, UserName, 'CHNStockMarket', 'BasicInfo')
            self.TradeDayTable = DatabaseTable(ServerName, UserName, 'CHNStockMarket', 'TradeDay')

        def UpdateBasicInfo(self):
            self.BasicInfoTable.CheckColumn({
                'CodeIDX': 'BIGINT NOT NULL',
                'Code': 'CHAR(16) NOT NULL',
                'Name': 'CHAR(16) NOT NULL',
                'Area': 'CHAR(8) NOT NULL',
                'Industry': 'CHAR(16) NOT NULL',
            }, Index=['CodeIDX'])

            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 

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

            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 

            TradeDay = self.API.trade_cal(exchange='', start_date='20000101', end_date=Date().SetTime(Month=12, Day=999).String(Style=Style_SS))

            Values = []
            for Item in TradeDay.itertuples():
                Values.append([int(Item.cal_date), int(Item.is_open)])
            
            self.TradeDayTable.DeleteAll()
            self.TradeDayTable.Insert(['Date', 'Open'], Values)

            self.UpdateManager.Update('TradeDay')
            print('TradeDay Updated')

        def UpdateStockTable(self):
            self.DB.CheckTable([Item[:6]+'_Price' for Item in self.AllStock()])


        def IsTradeDay(self, TestedDay):
            if type(TestedDay) == Date:
                TestedDay = TestedDay.String(Style=Style_SS)
            if not self.UpdateManager.TableUpdateTime('TradeDay'):
                self.UpdateTradeDay()

            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 

            Ret = self.TradeDayTable.SearchTable(Condition='''WHERE Date=%s'''%(TestedDay))

            if len(Ret) > 0:
                return True
            return False

        def LastTradeDay(self, TestedDay = None):
            if not TestedDay:
                TestedDay = Date()
            if TestedDay.HourInt() < 16:
                TestedDay = Date().ResetTime(Day=-1)

            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 

            if not self.UpdateManager.TableUpdateTime('TradeDay'):
                self.UpdateTradeDay()

            Ret = self.TradeDayTable.SearchTable(Condition='''WHERE Date<=%s AND Open = 1'''%(TestedDay.String(Style=Style_SS)), Column='''MAX(Date)''')
            return Ret[0][0]


        def AllStock(self, RawCode=False):
            if RawCode:
                return self.SZStock(RawCode=True) + self.ZXStock(RawCode=True) + self.SHStock(RawCode=True) + self.KCStock(RawCode=True)
            return self.SZStock() + self.ZXStock() + self.SHStock() + self.KCStock()
            print('Get All Stock Code')

        def SZStock(self, RawCode=False):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            if not self.UpdateManager.TableUpdateTime('BasicInfo'):
                self.UpdateBasicInfo()
            
            if RawCode:
                return [Item[2] for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<300000')]
            return [Item[2]+'.SZ' for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<300000')]

        def ZXStock(self, RawCode=False):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            if not self.UpdateManager.TableUpdateTime('BasicInfo'):
                self.UpdateBasicInfo()
            
            if RawCode:
                return [Item[2] for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<600000 AND CodeIDX>=300000')]
            return [Item[2]+'.SZ' for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<600000 AND CodeIDX>=300000')]

        def SHStock(self, RawCode=False):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            if not self.UpdateManager.TableUpdateTime('BasicInfo'):
                self.UpdateBasicInfo()

            if RawCode:
                return [Item[2] for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<680000 AND CodeIDX>=600000')]
            return [Item[2]+'.SH' for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<680000 AND CodeIDX>=600000')]

        def KCStock(self, RawCode=False):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 
            
            if not self.UpdateManager.TableUpdateTime('BasicInfo'):
                self.UpdateBasicInfo()

            if RawCode:
                return [Item[2] for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX>680000')]
            return [Item[2]+'.SH' for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX>680000')]


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
             
            self.TickTable = DatabaseTable(ServerName, UserName, 'CHNStockMarket', self.Code[:6]+'_Price')

        def GetSize(self):
            return self.TickTable.TableSize()
              
        def FullDownload(self):
            print(self.Code+' Full Download Start')
            self.TickTable.CheckColumn({
                'Date':             'INT NOT NULL',
                'Open':             'DECIMAL(13,4) NOT NULL',
                'High':             'DECIMAL(13,4) NOT NULL',
                'Low':              'DECIMAL(13,4) NOT NULL',
                'Close':            'DECIMAL(13,4) NOT NULL',
                'ChangedPrice':     'DECIMAL(13,4) NOT NULL',
                'ChangedPercent':   'DECIMAL(13,4) NOT NULL',
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
                    round(float(Item.open), 6),
                    round(float(Item.high), 6),
                    round(float(Item.low), 6),
                    round(float(Item.close), 6),
                    round(float(Item.change), 6),
                    round(float(Item.pct_chg), 6),
                    round(float(Item.vol), 6),
                    round(float(Item.amount), 6),
                    ])
            Values.reverse()

            self.TickTable.DeleteAll()
            self.TickTable.Insert(['Date', 'Open', 'High', 'Low', 'Close', 'ChangedPrice', 'ChangedPercent', 'Volume', 'Amount'], Values)

            self.UpdateManager.Update(self.Code[:6]+'_Price')
            print(self.Code+' Full Download Finished')

        def Sync(self):
            if not self.UpdateManager:
                self.UpdateManager = UpdateManager(DatabaseTable(self.ServerName, self.UserName, 'CHNStockMarket', 'UpdateInfo')) 

            if not self.UpdateManager.TableUpdateTime(self.Code[:6]+'_Price'):
                print(self.Code+' Sync FullDownload')
                self.FullDownload() 
                return
            
            print(self.Code+' Sync Update')
            if not self.StockMarket:
                self.StockMarket = CHN.StockMarket(self.ServerName, self.UserName)

            LastTradeDay = self.StockMarket.LastTradeDay()
            CurrentTradeDay = self.TickTable.SearchTable(Column='MAX(Date)')[0][0]

            if int(CurrentTradeDay) < int(LastTradeDay):
                print(self.Code+' Sync Ready To Update')
                RequestStart = Date(CurrentTradeDay).ResetTime(Day=1).String(Style=Style_SS)

                Tick = tushare.pro_bar(ts_code = self.Code, adj='qfq', start_date=str(RequestStart), end_date=str(LastTradeDay))

                Values = []
                for Item in Tick.itertuples():
                    Values.append([
                        int(Item.trade_date),
                        round(float(Item.open), 6),
                        round(float(Item.high), 6),
                        round(float(Item.low), 6),
                        round(float(Item.close), 6),
                        round(float(Item.change), 6),
                        round(float(Item.pct_chg), 6),
                        round(float(Item.vol), 6),
                        round(float(Item.amount), 6),
                        ])
                Values.reverse()

                self.TickTable.Insert(['Date', 'Open', 'High', 'Low', 'Close', 'ChangedPrice', 'ChangedPercent', 'Volume', 'Amount'], Values)

            print(self.Code+' Synchronize Finished')

        def GetOpen(self):
            pass

        def GetClose(self):
            pass

        def GetHigh(self):
            pass

        def GetLow(self):
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