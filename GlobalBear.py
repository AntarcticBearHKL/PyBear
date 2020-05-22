#----------------
#GlobalFunction:
#----------------
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

#================


#--------------
#GlobalConfig:
#--------------
import platform
GlobalDebugMode = False
GlobalAvailabilityCheck = False

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
AuthenticationOpenFunction = []
AuthenticationDatabaseName = 'Authentication'
AuthenticationMongoDBServerName = None
AuthenticationMongoDBUserName = None
AuthenticationRedisServerName = None
AuthenticationRedisUserName = None

#================

#---------
#WebDisk
#---------
DefaultWebDiskPort = 555

#=========


#-------------
#TimeCapsule:
#-------------
DefaultTimeCapsulePort = 715

#============



#---------
#Balance:
#---------
DefaultBalancePort = 1314

#=========



#----------
#HomePage:
#----------
DefaultHomePagePort = 443

#==========



#---------
#NoteBook:
#---------
DefaultNoteBookPort = 520

#=========


#------------
#WechatMPBE:
#------------
DefaultWechatMPBEPort = 443

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