from PyBear.GlobalBear import *
import redis

class Redis:
    def __init__(self, ServerName, UserName, DatabaseName=0, Decode=True):
        self.Connection = redis.StrictRedis(
            password = GetUser(UserName).Password, 
            host = GetServer(ServerName).IP, 
            port = GetServer(ServerName).Port,
            db = DatabaseName,
            decode_responses=Decode)

    def InsertString(self, Name, Value, px=None, nx=False, xx=False):
        if px:
            self.Connection.set(Name, Value, px=px, nx=nx, xx=xx)
        else:
            self.Connection.set(Name, Value, nx=nx, xx=xx)

    def InsertDict(self):
        pass

    def InsertSet(self):
        pass

    def InsertZSet(self):
        pass

    def Change(self):
        pass

    def Search(self, Condition):
        return self.Connection.keys(Condition)

    def Delete(self):
        pass