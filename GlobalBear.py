DebugMode = False
GlobalAvailabilityCheck = False

class BadBear(Exception):
    def __init__(self, Explain):
        self.Explain = Explain
    
    def __str__(self):
        return '----------------Error Happend----------------\n' + self.Explain

UserList = {}
class NewUser:
    def __init__(self, UserName, Password):
        self.UserName = UserName
        self.Password = Password
        UserList[UserName] = self
def GetUser(UserName):
    return UserList[UserName]

ServerList = {}
class NewServer:
    def __init__(self, ServerName, IP, Port):
        self.IP = IP
        self.Port = Port
        ServerList[ServerName] = self
def GetServer(ServerName):
    return ServerList[ServerName]