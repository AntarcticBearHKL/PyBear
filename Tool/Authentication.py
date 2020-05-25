import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Library.Cipher as CipherBear


def CreateUser(ServerName, ServiceName, Username, Password):
    if ExistUser(ServerName, ServiceName, UserName):
        print('User Exist')
        return
    UserTable = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)
    
    UserNumber = NewUserNumber()

    ServiceTable.Insert({
        'UserName':UserName,
        'Password':CipherBear.SHA256Encrypt(Password),
        'UserNumber':UserNumber,
        'Privilege':{},
    })

def ChangePassword():
    pass

def ExistUser(ServiceName, UserName):
    Table = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationMongoDBUserName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)

    Ret = Table.Search({"UserName" : UserName})
    if len(Ret) != 0:
        return True
    return False

def LoginUser(ServiceName, UserName, Password):
    ServiceTable = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationMongoDBUserName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)
    
    Ret = ServiceTable.Search({'UserName': UserName})[0]
    if Ret['Password'] == CipherBear.SHA256Encrypt(Password):
        LoginTable = RedisBear.Redis(
        GlobalBear.AuthenticationRedisServerName, 
        GlobalBear.AuthenticationRedisUserName, 
        )
        Status = CipherBear.UUID()
        LoginTable.set(Status, ServiceName+'/-/'+UserName, px=86400000)
        LoginTable.set(ServiceName+'/-/'+UserName, Status, px=86400000)
        return Status

def LogoutUser():
    pass

def UserAuthentication(ServiceName, Status):
    LoginTable = RedisBear.Redis(
    GlobalBear.AuthenticationRedisServerName, 
    GlobalBear.AuthenticationRedisUserName, 
    )
    return LoginTable.get(Status).split('/-/')[1]

def UserLogined(ServiceName, UserName):
    LoginTable = RedisBear.Redis(
    GlobalBear.AuthenticationRedisServerName, 
    GlobalBear.AuthenticationRedisUserName, 
    )

    if UserName in LoginTable.get(ServiceName+'/-/'+UserName):
        return True
    return False

def GrantUser():
    pass

def UserGranted():
    pass



Authentication_FunctionList = [
    'NewUserNumber', 
    'NewServiceToUser',
    'MergeUserNumber',
    'DeleteUser',
    'NewService',
    'NewServiceUser',
    'ChangePassword',
    'ServiceLogin',
    'ServiceLogout',
    'ServiceUserAuthentication',
    'IsUserLogin',
    'GrantUser',
    'IsUserGranted',
]