import os, sys
import json
import uuid

from PyBear.GlobalBear import *
from PyBear.Library.Time import *
from PyBear.Library.WebSuite import *
from PyBear.Library.Data.MySQL import *

def NewAuthenticationDatabase(Password, Port=3306):
    NewDatabasesServer['AuthenticationDatabaseServer'] = ['Authentication', Password, Port]

def CreateAccount(AdminAUID, Username, Password, ExpiredTime = 86400):
    if not AuthorityJudge(AccountAuthentication(AdminAUID, ExpiredTime=ExpiredTime), 'CreateAccount'):
        return Result(False, 'Permission Denied')

    if len(Username) < 6 or len(Password) < 6:
        return Result(False, 'Username Or Password Illegel')
    IdentificationDatabase = Database('AuthenticationDatabaseServer', 'Authentication')
    if len(IdentificationDatabase.Search('Identifications', 'Username', Username)) == 0:
        IdentificationDatabase.Insert('Identifications', {
            'Username':Username, 
            'Password':Password,
            })
        return Result(True, 'Sign Up Success')
    else:
        return Result(False, 'User Exist')

def AccountLogin(Username, Password):
    IdentificationDatabase = Database('AuthenticationDatabaseServer', 'Authentication')
    UserInfo = IdentificationDatabase.Search('Identifications', 'Username', Username)
    if len(UserInfo) == 1:
        if UserInfo[0][2] == Password:
            AUID = str(uuid.uuid1())
            IdentificationDatabase.Change('Identifications', 'Username', Username, 'AUID', AUID)
            IdentificationDatabase.Change('Identifications', 'Username', Username, 'Time', Date().String())
            return Result(AUID, 'Login Success')
        else:
            return Result(False, 'Password Wrong')
    else:
        return Result(False, 'User Does Not Exist')

def AccountAuthentication(AUID, ExpiredTime = 86400):
    IdentificationDatabase = Database('AuthenticationDatabaseServer', 'Authentication')
    SearchResult = IdentificationDatabase.Search('Identifications', 'AUID', AUID)
    if len(SearchResult) == 1:
        if (Date() - Date(SearchResult[0][4])) < ExpiredTime:
            return Result(SearchResult[0][1], SearchResult[0][1])
        else:
            return Result(False, 'Authentication Expire') 
    else: 
        return Result(False, 'Authentication Failed')

def AuthorityEndow(Username, AuthorityName):
    pass

def AuthorityJudge(Username, AuthorityName):
    if not Username:
        return False
    return True



AuthenticationServers = {}
def NewAuthenticationServer(Name, Ip, Port=6210):
    AuthenticationServers[Name] = [Ip, Port]