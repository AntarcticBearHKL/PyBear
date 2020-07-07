import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.Redis as RedisBear

class Config():
    def __init__(self, LogName):
        self.LogName = LogName

    def Run(self):
        Keys = RedisBear.Redis('RedisLocal').hgetall(self.LogName)
        for Key in Keys:
            print(Key, ': ', Keys[Key])