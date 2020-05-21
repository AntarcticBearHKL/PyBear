import PyBear.GlobalBear as GlobalBear
import redis

def Redis(ServerName, UserName, DatabaseName=0, Decode=True):
    return redis.StrictRedis(
        password = GetUser(UserName).Password, 
        host = GetServer(ServerName).IP, 
        port = GetServer(ServerName).Port,
        db = DatabaseName,
        decode_responses=Decode)