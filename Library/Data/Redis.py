import PyBear.GlobalBear as GlobalBear
import redis

def Redis(ServerName, DatabaseName=0, Decode=True):
    return redis.StrictRedis(
        password = GlobalBear.Server(ServerName).Password, 
        host = GlobalBear.Server(ServerName).IP, 
        port = GlobalBear.Server(ServerName).Port,
        db = DatabaseName,
        decode_responses=Decode)