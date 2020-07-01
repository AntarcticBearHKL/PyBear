#----------------
#GlobalFunction:
#----------------
class BadBear(Exception):
    def __init__(self, Explain):
        self.Explain = Explain
    
    def Except(self):
        if callable(self.Explain):
            return self.Explain()
        return self.Explain

def CatchBadBear(Fn, *args, **kwargs):
    def Ret(*args, **kwargs):
        try:
            Fn(*args, **kwargs)
        except BadBear as Error:
            Error.Except()
    return Ret


ServerList = {}
class NewServer:
    def __init__(self, ServerName, IP, Port, Username, Password):
        self.IP = IP
        self.Port = Port
        self.Username = Username
        self.Password = Password
        ServerList[ServerName] = self
def Server(ServerName):
    return ServerList[ServerName]

LocationList = {}
class NewLocation:
    def __init__(self, LocationName, Location):
        self.Location = Location
        LocationList[LocationName] = self
def Location(LocationName):
    return LocationList[LocationName].Location

#================


#--------------
#GlobalConfig:
#--------------
import platform
GlobalDebugMode = False
GlobalTestModuleOn = False
import time
import datetime
StartTime = datetime.datetime.now()
LocalTimeZoneShift = int(int(time.strftime('%z'))/100)
def UpTime():
    print(datetime.datetime.now() - StartTime)

NewServer(
    'Mysql', '47.95.119.172', 3306,
    'Debuger', 'A11b22;;')
NewServer(
    'MongoDB', '47.95.119.172', 27017,
    'Debuger', 'A11b22;;')
NewServer(
    'Redis', '47.95.119.172', 6379,
    'Debuger', 'A11b22;;')

if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    NewLocation('DefaultCertificationFileLocation', 'E:\GitHub\BearApplication\PythonApplication/Certification/www.bear-services.com')

elif platform.system() == "Linux":
    NewLocation('DefaultCertificationFileLocation', '/BearApplication/PythonApplication/Certification/www.bear-services.com')

#==============


#----------------
#Authentication:
#----------------
AuthenticationName = 'Authentication'
AuthenticationPort = 621
AuthenticationDatabaseName = 'Authentication'

#================


#-------------
#TimeCapsule:
#-------------
TimeCapsuleName = 'TimeCapsule'
TimeCapsulePort = 715
TimeCapsuleDatabaseName = 'TimeCapsule'
#============



#----------
#HomePage:
#----------
HomePagePort = 443

#==========


#------------
#WechatMPBE:
#------------
WechatMPPort = 443

#============

#------------
#BearSearch:
#------------
BearSearchPort = 233

#============


#------------
#FinancialMarket:
#------------
TushareToken = '85eca8e96158d3127814bcde6bf4c000326799ae66b54030d51ccde5'

#============


#--------------
#GlobalConfig:
#--------------
BearModule = [
    'tensorflow',
    'scikit-learn',
    'statsmodels',
    'pymysql',
    'pyecharts',
    'tushare',
    'requests-html',
    'scipy',
    'python-dateutil',
    'tornado',
    'wxpy',
    'cryptography',
    'talib',
    'pymongo',
    'redis',
    'pycryptodome',
    'jieba',
    'nltk',
]

#==============