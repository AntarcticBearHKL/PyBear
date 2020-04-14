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
    tushare.set_token(token)
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

            self.CHNStockMarketDataBase = Database(ServerName, UserName, 'CHNStockMarket')

            self.CHNStockMarketDataBase.CheckTable([
                'BasicInfo',
                'TradeDay',
                'UpdateInfo',
            ])

            self.BasicInfoTable = self.CHNStockMarketDataBase.Table('BasicInfo')
            self.TradeDayTable = self.CHNStockMarketDataBase.Table('TradeDay')
            self.UpdateInfoTable = self.CHNStockMarketDataBase.Table('UpdateInfo')
            self.UpdateManager = UpdateManager(self.UpdateInfoTable)

        def UpdateBasicInfo(self):
            print('BasicInfo Update Start')
            self.BasicInfoTable.CheckColumn({
                'CodeIDX': 'BIGINT NOT NULL',
                'Code': 'CHAR(16) NOT NULL',
                'Name': 'CHAR(16) NOT NULL',
                'Area': 'CHAR(8) NOT NULL',
                'Industry': 'CHAR(16) NOT NULL',
            }, Index=['CodeIDX'])

            BasicInfo = self.API.stock_basic()

            Values = []
            for Item in BasicInfo.itertuples():
                Values.append([int(Item.symbol), Item.symbol, Item.name, Item.area, Item.industry])
            
            self.BasicInfoTable.DeleteAll()
            self.BasicInfoTable.Insert(['CodeIDX', 'Code', 'Name', 'Area', 'Industry'], Values)

            self.UpdateManager.Update('BasicInfo')
            print('BasicInfo Update Finished')

        def UpdateTradeDay(self, latest=False):
            print('TradeDay Update Start')
            self.TradeDayTable.CheckColumn({
                'Date': 'INT NOT NULL',
                'Open': 'INT NOT NULL',
            }, Index=['Date'])

            TradeDay = self.API.trade_cal(exchange='', start_date='20000101', end_date=Date().SetTime(Month=12, Day=999).String(Style=Style_SS))

            Values = []
            for Item in TradeDay.itertuples():
                Values.append([int(Item.cal_date), int(Item.is_open)])
            
            self.TradeDayTable.DeleteAll()
            self.TradeDayTable.Insert(['Date', 'Open'], Values)

            self.UpdateManager.Update('TradeDay')
            print('TradeDay Update Finished')

        def CheckStockTable(self):
            self.DB.CheckTable([Item[:6]+'_Price' for Item in self.AllStock()])


        def IsTradeDay(self, TestedDay):
            if type(TestedDay) == Date:
                TestedDay = TestedDay.String(Style=Style_SS)

            Ret = self.TradeDayTable.SearchTable(Condition='''WHERE Date=%s'''%(TestedDay))

            if len(Ret) > 0:
                return True
            return False

        def LastTradeDay(self, TestedDay = None):
            if not TestedDay:
                TestedDay = Date()
            if TestedDay.HourInt() < 16:
                TestedDay = Date().ResetTime(Day=-1)

            Ret = self.TradeDayTable.SearchTable(Condition='''WHERE Date<=%s AND Open = 1'''%(TestedDay.String(Style=Style_SS)), Column='''MAX(Date)''')
            return Ret[0][0]

        def GetTradeDay(self, Start=None, End=None, Day=None):
            if Start and End:
                Ret = self.TradeDayTable.SearchTable(Condition='''WHERE Date>=%s AND Date<=%s AND Open = 1 ORDER BY Date ASC'''%(Start.String(Style=Style_SS), End.String(Style=Style_SS)), Column='Date')
                return [Item[0] for Item in Ret]
            elif Start and Day:
                Ret = self.TradeDayTable.SearchTable(Condition='''WHERE Date>=%s AND Open = 1 ORDER BY Date ASC'''%(Start.String(Style=Style_SS)), Column='Date')
                return [Item[0] for Item in Ret][:Day]
            elif End and Day:
                Ret = self.TradeDayTable.SearchTable(Condition='''WHERE Date<=%s AND Open = 1 ORDER BY Date DESC LIMIT %s'''%(End().String(Style=Style_SS), Day), Column='Date')
                Ret = [Item[0] for Item in Ret]
                Ret.reverse()
                return Ret
            elif Day:
                Ret = self.TradeDayTable.SearchTable(Condition='''WHERE Date<=%s AND Open = 1 ORDER BY Date DESC LIMIT %s'''%(Date().String(Style=Style_SS), Day), Column='Date')
                Ret = [Item[0] for Item in Ret]
                Ret.reverse()
                return Ret
            else:
                raise BadBear('--------GetTradeDay Para Error---------')


        def AllStock(self, RawCode=False):
            if RawCode:
                return self.SZStock(RawCode=True) + self.ZXStock(RawCode=True) + self.SHStock(RawCode=True) + self.KCStock(RawCode=True)
            return self.SZStock() + self.ZXStock() + self.SHStock() + self.KCStock()
            print('Get All Stock Code')

        def SZStock(self, RawCode=False):
            if self.BasicInfoTable.GetRowNumber == 0:
                self.UpdateBasicInfo()

            if RawCode:
                return [Item[2] for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<300000')]
            return [Item[2]+'.SZ' for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<300000')]

        def ZXStock(self, RawCode=False):
            if self.BasicInfoTable.GetRowNumber == 0:
                self.UpdateBasicInfo()
            
            if RawCode:
                return [Item[2] for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<600000 AND CodeIDX>=300000')]
            return [Item[2]+'.SZ' for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<600000 AND CodeIDX>=300000')]

        def SHStock(self, RawCode=False):
            if self.BasicInfoTable.GetRowNumber == 0:
                self.UpdateBasicInfo()
            

            if RawCode:
                return [Item[2] for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<680000 AND CodeIDX>=600000')]
            return [Item[2]+'.SH' for Item in self.BasicInfoTable.SearchTable(Condition='WHERE CodeIDX<680000 AND CodeIDX>=600000')]

        def KCStock(self, RawCode=False):
            if self.BasicInfoTable.GetRowNumber == 0:
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
            if TushareAvailiable:
                raise BadBear('Tushare Cannot Use Without Token')
            self.ServerName = ServerName
            self.UserName = UserName
            self.Code = Code
            self.StockMarket = None
             
            self.TickTable = DatabaseTable(ServerName, UserName, 'CHNStockMarket', self.Code[:6]+'_Price')


        def Sync(self, LastTradeDay):
            if self.NeedFullDownload():
                print(self.Code+' Sync Full Download')
                self.FullDownload() 
                return

            (UpdateCheck, Start, End) = self.NeedUpdate(LastTradeDay)
            if UpdateCheck:
                print(self.Code+' Sync Update')
                self.Update(Start, End)

            print(self.Code+' Synchronize Finished')

        def FullDownload(self):
            print(self.Code+' Full Download Start')
            self.TickTable.CheckColumn({
                'Date':             'INT NOT NULL DEFAULT 0',
                'Open':             'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'High':             'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'Low':              'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'Close':            'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'ChangedPrice':     'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'ChangedPercent':   'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'Volume':           'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'Amount':           'DECIMAL(13,4) NOT NULL DEFAULT 0',
            }, Index=['Date'])

            Tick = tushare.pro_bar(ts_code = self.Code, adj='qfq', start_date='20050101', end_date=Date().String(Style='SS')).dropna()
            print(Tick)

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

            print(self.Code+' Full Download Finished')

        def Update(self, Start, End):
            Tick = tushare.pro_bar(ts_code = self.Code, adj='qfq', start_date=Start, end_date=End)

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

        def NeedFullDownload(self):
            if self.TickTable.GetRowNumber() == 0:
                return True
            return False

        def NeedUpdate(self, LastTradeDay):
            CurrentTradeDay = self.TickTable.SearchTable(Column='MAX(Date)')[0][0]

            if int(CurrentTradeDay) < int(LastTradeDay):
                RequestStart = Date(CurrentTradeDay).ResetTime(Day=1).String(Style=Style_SS)
                return True, str(RequestStart), str(LastTradeDay)
            return False, '', ''

        def IsAvailable(self, LastTradeDay):
            if Stock.NeedFullDownload() or Stock.NeedUpdate(LastTradeDay)[0]:
                return False
            return True


        def GetData(self, Start, End, DataName):
            Result = self.TickTable.SearchTable(Column=DataName, Condition='''WHERE Date>=%s AND Date<=%s'''%(Start, End))
            Ret = []
            for Item in Result:
                Ilist = []
                for Itemm in Item:
                    Ilist.append(float(Itemm))
                Ret.append(Ilist)
            return Ret


        def GetTableSize(self):
            return self.TickTable.GetTableSize()

        def GetRowNumber(self):
            return self.TickTable.GetRowNumber()
              
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
    def Profit(Data, Days):
        return Data[-1] - Data[-1-Days]


    def MA(Data, days=120, range=5):
        return talib.MA(numpy.array(self.stockInfo.getOpen(days=days)), timeperiod=range) 

    def EMA(Data, days=120, range=5):
        return talib.EMA(numpy.array(self.stockInfo.getOpen(days=days)), timeperiod=range) 

    def BOLL(Data, days=120, range=5):
        pass

    def MACD(Data, fastperiod=12, slowperiod=26, signalperiod=9):
        DIF, DEA, MACD = talib.MACD(
        numpy.array(Data),
        fastperiod=fastperiod, 
        slowperiod=slowperiod, 
        signalperiod=signalperiod)
        return DIF, DEA, MACD*2

    def RSV(Close, High, Low):
        return talib.STOCH(
            numpy.array(High),
            numpy.array(Low),
            numpy.array(Close),
            fastk_period = 1,
            slowk_period = 1,
            slowk_matype = 0,
            slowd_period = 5,
            slowd_matype = 0,)

    def RSI(Data, days=120, range=5):
        return talib.RSI(numpy.array(self.stockInfo.getOpen(days=days)), 5)

    def GetCDLIndex(Open, High, Low, Close):
        Open = numpy.array(Open)
        High = numpy.array(High)
        Low = numpy.array(Low)
        Close = numpy.array(Close)
        CDLIndex = []
        CDLIndex.append(talib.CDL2CROWS(Open, High, Low, Close))
        CDLIndex.append(talib.CDL3BLACKCROWS(Open, High, Low, Close))
        CDLIndex.append(talib.CDL3INSIDE(Open, High, Low, Close))
        CDLIndex.append(talib.CDL3LINESTRIKE(Open, High, Low, Close))
        CDLIndex.append(talib.CDL3OUTSIDE(Open, High, Low, Close))
        CDLIndex.append(talib.CDL3STARSINSOUTH(Open, High, Low, Close))
        CDLIndex.append(talib.CDL3WHITESOLDIERS(Open, High, Low, Close))
        CDLIndex.append(talib.CDLABANDONEDBABY(Open, High, Low, Close))
        CDLIndex.append(talib.CDLADVANCEBLOCK(Open, High, Low, Close))
        CDLIndex.append(talib.CDLBELTHOLD(Open, High, Low, Close))
        CDLIndex.append(talib.CDLBREAKAWAY(Open, High, Low, Close))
        CDLIndex.append(talib.CDLCLOSINGMARUBOZU(Open, High, Low, Close))
        CDLIndex.append(talib.CDLCONCEALBABYSWALL(Open, High, Low, Close))
        CDLIndex.append(talib.CDLCOUNTERATTACK(Open, High, Low, Close))
        CDLIndex.append(talib.CDLDARKCLOUDCOVER(Open, High, Low, Close))
        CDLIndex.append(talib.CDLDOJI(Open, High, Low, Close))
        CDLIndex.append(talib.CDLDOJISTAR(Open, High, Low, Close))
        CDLIndex.append(talib.CDLDRAGONFLYDOJI(Open, High, Low, Close))
        CDLIndex.append(talib.CDLENGULFING(Open, High, Low, Close))
        CDLIndex.append(talib.CDLEVENINGDOJISTAR(Open, High, Low, Close))
        CDLIndex.append(talib.CDLEVENINGSTAR(Open, High, Low, Close))
        CDLIndex.append(talib.CDLGAPSIDESIDEWHITE(Open, High, Low, Close))
        CDLIndex.append(talib.CDLGRAVESTONEDOJI(Open, High, Low, Close))
        CDLIndex.append(talib.CDLHAMMER(Open, High, Low, Close))
        CDLIndex.append(talib.CDLHANGINGMAN(Open, High, Low, Close))
        CDLIndex.append(talib.CDLHARAMI(Open, High, Low, Close))
        CDLIndex.append(talib.CDLHARAMICROSS(Open, High, Low, Close))
        CDLIndex.append(talib.CDLHIGHWAVE(Open, High, Low, Close))
        CDLIndex.append(talib.CDLHIKKAKE(Open, High, Low, Close))
        CDLIndex.append(talib.CDLHIKKAKEMOD(Open, High, Low, Close))
        CDLIndex.append(talib.CDLHOMINGPIGEON(Open, High, Low, Close))
        CDLIndex.append(talib.CDLIDENTICAL3CROWS(Open, High, Low, Close))
        CDLIndex.append(talib.CDLINNECK(Open, High, Low, Close))
        CDLIndex.append(talib.CDLINVERTEDHAMMER(Open, High, Low, Close))
        CDLIndex.append(talib.CDLKICKING(Open, High, Low, Close))
        CDLIndex.append(talib.CDLKICKINGBYLENGTH(Open, High, Low, Close))
        CDLIndex.append(talib.CDLLADDERBOTTOM(Open, High, Low, Close))
        CDLIndex.append(talib.CDLLONGLEGGEDDOJI(Open, High, Low, Close))
        CDLIndex.append(talib.CDLLONGLINE(Open, High, Low, Close))
        CDLIndex.append(talib.CDLMARUBOZU(Open, High, Low, Close))
        CDLIndex.append(talib.CDLMATCHINGLOW(Open, High, Low, Close))
        CDLIndex.append(talib.CDLMATHOLD(Open, High, Low, Close))
        CDLIndex.append(talib.CDLMORNINGDOJISTAR(Open, High, Low, Close))
        CDLIndex.append(talib.CDLMORNINGSTAR(Open, High, Low, Close))
        CDLIndex.append(talib.CDLONNECK(Open, High, Low, Close))
        CDLIndex.append(talib.CDLPIERCING(Open, High, Low, Close))
        CDLIndex.append(talib.CDLRICKSHAWMAN(Open, High, Low, Close))
        CDLIndex.append(talib.CDLRISEFALL3METHODS(Open, High, Low, Close))
        CDLIndex.append(talib.CDLSEPARATINGLINES(Open, High, Low, Close))
        CDLIndex.append(talib.CDLSHOOTINGSTAR(Open, High, Low, Close))
        CDLIndex.append(talib.CDLSHORTLINE(Open, High, Low, Close))
        CDLIndex.append(talib.CDLSPINNINGTOP(Open, High, Low, Close))
        CDLIndex.append(talib.CDLSTALLEDPATTERN(Open, High, Low, Close))
        CDLIndex.append(talib.CDLSTICKSANDWICH(Open, High, Low, Close))
        CDLIndex.append(talib.CDLTAKURI(Open, High, Low, Close))
        CDLIndex.append(talib.CDLTASUKIGAP(Open, High, Low, Close))
        CDLIndex.append(talib.CDLTHRUSTING(Open, High, Low, Close))
        CDLIndex.append(talib.CDLTRISTAR(Open, High, Low, Close))
        CDLIndex.append(talib.CDLUNIQUE3RIVER(Open, High, Low, Close))
        CDLIndex.append(talib.CDLUPSIDEGAP2CROWS(Open, High, Low, Close))
        CDLIndex.append(talib.CDLXSIDEGAP3METHODS(Open, High, Low, Close))

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

class Brokor:
    def __init__(self, Date, Data):
        for Item in Data:
            if len(Item) != len(Date):
                raise BadBear('Broker Data Not Synchronous')

        self.DateIndex = {}
        self.Date = Date
        self.Data = Data
        IndexNumber = 0
        for Item in Date:
            self.DateIndex[Item] = IndexNumber
            IndexNumber += 1

        MinList = []
        MaxList = []
        for Item in self.Data:
            CounterList = []
            for Counter in range(len(Item)):
                if type(Item[Counter]) != list and numpy.isnan(Item[Counter]):
                    continue
                CounterList.append(Counter)
            MinList.append(min(CounterList))
            MaxList.append(max(CounterList))

        self.Start = max(MinList)
        self.End = min(MaxList)
        if self.Start > self.End:
            raise BadBear('Broker Data Not Enough')
        self.Pointer = self.Start - 1

    def __len__(self):
        return self.End - self.Start + 1

    def __iter__(self):
        return self

    def __next__(self):
        self.Pointer += 1
        if self.Pointer > self.End:
            raise StopIteration
        Ret = [self.Pointer, self.Date[self.Pointer]]
        for Item in self.Data:
            Ret.append(Item[self.Pointer])
        return Ret

    def Inspect(self, Start=None, End=None):
        if Start and End:
            pass
        elif Start:
            pass

    def GetInfo(self, Pointer, Force = False):
        if not Force:
            if Pointer > self.End:
                raise BadBear('Brokor Pointer Exceed End')
        Ret = [Pointer, Date[Pointer]]
        for Item in self.Data:
            Ret.append(Item[Pointer])
        return Ret

class Analyst:
    def DailyUpdate(ServerName, UserName):
        TM = TaskMatrix(2,16, LimitPerMinute=245)
        CHNStockMarket = CHN.StockMarket(ServerName, UserName)

        LTD = CHNStockMarket.LastTradeDay()

        CacheList = TM.GetCacheList()

        StockArg = [[ServerName, UserName, Item, LTD, CacheList] for Item in CHNStockMarket.AllStock()]
        print('Ready To Launch')

        TM.ImportTask(WorkLoad.StockUpdate, StockArg)
        TM.Start()

        print(CacheList)

    def NeedUpdate(ServerName, UserName):
        TM = TaskMatrix(2,16)
        CHNStockMarket = CHN.StockMarket(ServerName, UserName)

        LTD = CHNStockMarket.LastTradeDay()

        CacheList = TM.GetCacheList()

        StockArg = [[ServerName, UserName, Item, LTD, CacheList] for Item in CHNStockMarket.AllStock()]
        print('Ready To Launch')

        TM.ImportTask(WorkLoad.NeedUpdate, StockArg)
        TM.Start()

        print(CacheList)
            

class WorkLoad:
    def StockUpdate(ServerName, UserName, StockCode, LastTradeDay, CacheList):
        ErrorCounter = 0
        while True:
            try:
                CHN.Stock(ServerName, UserName, StockCode).Sync(LastTradeDay)
                break
            except Exception as e:
                ErrorCounter += 1
                if ErrorCounter >= 10:
                    print(e)
                    print('''ERROR HAPPEND: %s''' % (StockCode))
                    CacheList.append(StockCode)
                    break

    def NeedUpdate(ServerName, UserName, StockCode, LastTradeDay, CacheList):
        ErrorCounter = 0
        while True:
            try:
                print(StockCode)
                Stock = CHN.Stock(ServerName, UserName, StockCode)
                if Stock.NeedFullDownload() or Stock.NeedUpdate(LastTradeDay)[0]:
                    CacheList.append(StockCode)
                break
            except Exception as e:
                ErrorCounter += 1
                if ErrorCounter >= 10:
                    print(e)
                    print('''ERROR HAPPEND: %s''' % (StockCode))
                    CacheList.append('ERROR: ' + StockCode)
                    break