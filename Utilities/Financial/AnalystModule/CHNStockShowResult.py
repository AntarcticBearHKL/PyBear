import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Utilities.Financial.Analyst as AnalystBear

class Config(AnalystBear.AnalystModule):
    def __init__(self, LogName):
        self.LogName = LogName

    def Run(self):
        Keys = RedisBear.Redis('RedisLocal').hgetall(self.LogName)
        Keylist = list(Keys)
        Keylist.sort()
        for Key in Keylist:
            print(Key, ': ', Keys[Key])