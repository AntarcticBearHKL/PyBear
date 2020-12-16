import PyBear.Bear as Bear
import redis

def Redis(ServerName, DatabaseName=0, Decode=True):
    return redis.StrictRedis(
        password = Bear.Server(ServerName).Password, 
        host = Bear.Server(ServerName).IP, 
        port = Bear.Server(ServerName).Port,
        db = DatabaseName,
        decode_responses=Decode)