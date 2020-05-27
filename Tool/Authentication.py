import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Library.Cipher as CipherBear


def CreateUser(ServerName, ServiceName, Username, Password):
    if ExistUser(ServerName, ServiceName, UserName):
        print('User Exist')
        return
    Table = MongoDBBear.MongoDBTable(
        ServerName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)

    Table.Insert({
        'UserName':UserName,
        'Password':CipherBear.SHA256Encrypt(Password),
        'Privilege':{},
    })

def ChangePassword():
    pass

def ExistUser(ServerName, ServiceName):
    Table = MongoDBBear.MongoDBTable(
        ServerName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)

    Ret = Table.Search({"UserName" : UserName})
    if len(Ret) != 0:
        return True
    return False

def LoginUser(ServerName, ServiceName, UserName, Password, ExpireTime=86400000):
    Table = MongoDBBear.MongoDBTable(
        ServerName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)
    
    Ret = Table.Search({'UserName': UserName})[0]
    if Ret['Password'] == CipherBear.SHA256Encrypt(Password):
        LoginTable = RedisBear.Redis(ServerName)
        AuthenticationCode = CipherBear.UUID()
        LoginTable.set(AuthenticationCode, ServiceName+'/-/'+UserName, px=ExpireTime)
        LoginTable.set(ServiceName+'/-/'+UserName, AuthenticationCode, px=ExpireTime)
        return AuthenticationCode

def LogoutUser():
    pass

def UserAuthentication(ServerName, ServiceName, AuthenticationCode):
    Result = RedisBear.Redis(ServerName).get(AuthenticationCode)
    if Result:
        Result = Result.split('/-/')
        if Result[0] == ServiceName:
            return Result.split('/-/')[1]
    return None

def UserLogined(ServiceName, UserName):
    RedisBear.Redis(ServerName)
    if UserName in LoginTable.get(ServiceName+'/-/'+UserName):
        return True
    return False

def GrantUser():
    pass

def UserGranted():
    pass