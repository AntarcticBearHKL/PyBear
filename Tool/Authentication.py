import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Library.Cipher as CipherBear


def InitMongoDB(ServerName, UserName):
    GlobalBear.AuthenticationMongoDBServerName = ServerName
    GlobalBear.AuthenticationMongoDBUserName = UserName

def InitRedis(ServerName, UserName):
    GlobalBear.AuthenticationRedisServerName = ServerName
    GlobalBear.AuthenticationRedisUserName = UserName

def NewUserNumber():
    Table = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationMongoDBUserName, 
        GlobalBear.AuthenticationDatabaseName, 
        'UserCenter')

    UserNumber = CipherBear.UUID()
    Table.Insert({
        'UserNumber': UserNumber,
        'Service': {},
    })
    return UserNumber

def NewServiceToUser(UserNumber, ServiceName, UserName):
    if not UserExist(UserNumber):
        return
    Table = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationMongoDBUserName, 
        GlobalBear.AuthenticationDatabaseName, 
        'UserCenter')

    Service = Table.Search({"UserNumber" : UserNumber,})[0]['Service']
    Service[ServiceName] = UserName

    Table.Change(
        {
            "UserNumber" : UserNumber,
        },
        {
            '$set':{
                'Service':Service
            }
        }
    )

def UserExist(UserNumber):
    Table = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationMongoDBUserName, 
        GlobalBear.AuthenticationDatabaseName, 
        'UserNumber')

    Ret = Table.Search({"UserNumber" : UserNumber})
    if len(Ret) != 0:
        return True
    return False

def MergeUserNumber():
    pass

def DeleteUser(UserNumber):
    #!!判断所有服务都停用
    Table = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationMongoDBUserName, 
        GlobalBear.AuthenticationDatabaseName, 
        'UserNumber')

    Table.Delete({"UserNumber" : UserNumber})



def NewServiceUser(ServiceName, UserName, Password):
    if ServiceUserExist(ServiceName, UserName):
        return
    ServiceTable = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationMongoDBUserName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)
    
    UserNumber = NewUserNumber()

    ServiceTable.Insert({
        'UserName':UserName,
        'Password':CipherBear.SHA256Encrypt(Password),
        'UserNumber':UserNumber,
        'Privilege':{},
    })

    NewServiceToUser(UserNumber, ServiceName, UserName)

def ChangePassword():
    pass

def ServiceUserExist(ServiceName, UserName):
    Table = MongoDBBear.MongoDBTable(
        GlobalBear.AuthenticationMongoDBServerName, 
        GlobalBear.AuthenticationMongoDBUserName, 
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)

    Ret = Table.Search({"UserName" : UserName})
    if len(Ret) != 0:
        return True
    return False

def ServiceLogin(ServiceName, UserName, Password):
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

def ServiceLogout():
    pass

def ServiceUserAuthentication(ServiceName, Status):
    LoginTable = RedisBear.Redis(
    GlobalBear.AuthenticationRedisServerName, 
    GlobalBear.AuthenticationRedisUserName, 
    )
    return LoginTable.get(Status).split('/-/')[1]

def IsUserLogin(ServiceName, UserName):
    LoginTable = RedisBear.Redis(
    GlobalBear.AuthenticationRedisServerName, 
    GlobalBear.AuthenticationRedisUserName, 
    )

    if UserName in LoginTable.get(ServiceName+'/-/'+UserName):
        return True
    return False

def GrantUser():
    pass

def IsUserGranted():
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