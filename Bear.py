#------------------------
#GlobalFunction:
#------------------------

class Result:
    def __init__(self, Code, Explaination = None):
        self.Code = Code
        self.Explaination = Explaination

def CatchResult(Input=None, Restrict = True):
    if type(Input) != Result:
        if Restrict:
            assert 0
        else:
            return Input
    if Input.Explaination:
        print(Input.Explaination)
    return Input.Code


class BadBear(Exception):
    def __init__(self, Explain):
        self.Explain = Explain
    
    def Except(self):
        if callable(self.Explain):
            return Result(-1, self.Explain())
        return Result(-1, self.Explain)

def CatchBadBear(Fn, *args, **kwargs):
    def Ret(*args, **kwargs):
        if Debug:
            return Fn(*args, **kwargs)
        else:    
            try:
                return Fn(*args, **kwargs)
            except BadBear as Error:
                return Error.Except()
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
Debug = True

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

#=========================