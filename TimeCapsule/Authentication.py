import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Library.Cipher as CipherBear


def CreateUser(ServerName, ServiceName, Username, Password):
    if ExistUser(ServerName, ServiceName, Username):
        print('User Exist')
        return
    Table = MongoDBBear.MongoDB(
        ServerName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)

    Table.Insert({
        'Username':Username,
        'Password':CipherBear.SHA256Encrypt(Password),
        'Privilege':{},
    })

def ChangePassword():
    pass

def ExistUser(ServerName, ServiceName, Username):
    Table = MongoDBBear.MongoDB(
        ServerName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)

    Ret = Table.Search({"Username" : Username})
    if len(Ret) != 0:
        return True
    return False

def LoginUser(MongoServerName, RedisServerName, ServiceName, Username, Password, ExpireTime=86400000):
    Table = MongoDBBear.MongoDB(
        MongoServerName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)
    
    Ret = Table.Search({'Username': Username})[0]
    if Ret['Password'] == CipherBear.SHA256Encrypt(Password):
        LoginTable = RedisBear.Redis(RedisServerName)
        AuthenticationCode = CipherBear.UUID()
        LoginTable.set(AuthenticationCode, ServiceName+'/-/'+Username, px=ExpireTime)
        LoginTable.set(ServiceName+'/-/'+Username, AuthenticationCode, px=ExpireTime)
        return AuthenticationCode

def LogoutUser():
    pass

def UserAuthentication(ServerName, AuthenticationCode):
    Result = RedisBear.Redis(ServerName).get(AuthenticationCode)
    if Result:
        Result = Result.split('/-/')
        return Result[0], Result[1]
    return None, None

def UserLogined(ServerName, ServiceName, Username):
    if RedisBear.Redis(ServerName).get(ServiceName+'/-/'+Username):
        return True
    return False

def GrantUser():
    pass

def UserGranted():
    pass

if GlobalBear.GlobalTestModuleOn:
    pass