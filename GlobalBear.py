DebugMode = False
GlobalAvailabilityCheck = False

class BadBear(Exception):
    def __init__(self, Explain):
        self.Explain = Explain
    
    def __str__(self):
        return '----------------Error Happend----------------\n' + self.Explain

def CatchBadBear(Fn, *args, **kwargs):
    def Ret(*args, **kwargs):
        try:
            Fn(*args, **kwargs)
        except BadBear as Error:
            print(Error)
    return Ret



UserList = {}
class NewUser:
    def __init__(self, UserName, Password):
        self.UserName = UserName
        self.Password = Password
        UserList[UserName] = self
def GetUser(UserName):
    return UserList[UserName]

ServerList = {}
class NewServer:
    def __init__(self, ServerName, IP, Port):
        self.IP = IP
        self.Port = Port
        ServerList[ServerName] = self
def GetServer(ServerName):
    return ServerList[ServerName]

LocationList = {}
class NewLocation:
    def __init__(self, LocationName, Location):
        self.Location = Location
        LocationList[LocationName] = self
def GetLocation(LocationName):
    return LocationList[LocationName].Location



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
    'talib'
]

BearPort = {
    'Authentication': 2333,
    'HomePageHTTP': 80,
    'HomePageHTTPS': 443,
    'WechatMPBE', 443
}