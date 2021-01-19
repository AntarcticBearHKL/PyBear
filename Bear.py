# -*- coding: utf-8 -*-  

#------------------------
#GlobalFunction:
#------------------------
def Result(Code, Message):
    print(Message)
    return Code

class BadBear(Exception):
    def __init__(self, SolveFunction):
        self.SolveFunction = SolveFunction
    
    def Solve(self):
        return self.SolveFunction()

def CatchBadBear(Fn, *args, **kwargs):
    def Ret(*args, **kwargs): 
        return Fn(*args, **kwargs)
        if Debug:
            try:
                return Fn(*args, **kwargs)
            except BadBear as Error:
                return Error.Solve()
        else:
            try:
                return Fn(*args, **kwargs)
            except BadBear as Error:
                return Error.Solve()    
            except Exception as OtherError:
                print(OtherError)
    return Ret


ServerList = {}
class NewServer:
    def __init__(self, ServerName, Key, ServerCode):
        import PyBear.Math.Cipher as Cipher
        self.IP = Cipher.AESDecrypt(ServerCode[:44], Key)
        self.Port = int(Cipher.AESDecrypt(ServerCode[44:88], Key))
        self.Username = Cipher.AESDecrypt(ServerCode[88:132], Key)
        self.Password = Cipher.AESDecrypt(ServerCode[132:], Key)
        ServerList[ServerName] = self
def Server(ServerName):
    return ServerList[ServerName]
def GenerateServerCode(Key, IP, Port, Username, Password):
    import PyBear.Math.Cipher as Cipher
    Ret = ''
    Ret += Cipher.AESEncrypt(IP, Key)
    Ret += Cipher.AESEncrypt(Port, Key)
    Ret += Cipher.AESEncrypt(Username, Key)
    Ret += Cipher.AESEncrypt(Password, Key)
    return Ret


LocationList = {}
class NewLocation:
    def __init__(self, LocationName, Location):
        self.Location = Location
        LocationList[LocationName] = self
def Location(LocationName):
    return LocationList[LocationName].Location

#=========================


#------------------------
#GlobalConfig:
#------------------------
TestUnit = False
Debug = False

import time
import datetime
StartTime = datetime.datetime.now()
LocalTimeZoneShift = int(int(time.strftime('%z'))/100)
def UpTime():
    print(datetime.datetime.now() - StartTime)


import platform
if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

elif platform.system() == "Linux":
    pass

#=========================


#------------------------
#FinancialMarket:
#------------------------
TushareToken = '85eca8e96158d3127814bcde6bf4c000326799ae66b54030d51ccde5'

#=========================


#------------------------
#GlobalConfig:
#------------------------
a = 'tensorflow'
BearModule = [
    'TA-lib',
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

#=========================