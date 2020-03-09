import os, sys
from wxpy import *

from PyBear.GlobalBear import *
from PyBear.Library.Chronus import *
from PyBear.Library.Data.File import *

WechatHistoryFileLocation = {}
def NewWechatHistoryFileLocation(Name, Dir):
    WechatHistoryFileLocation[Name] = Dir


class WechatWraper():
    def __init__(self, cache_path):
        self.start
        self.bot = Bot(cache_path= cache_path)
        self.MessageHandler = self.bot.register
        self.FriendList = None
        self.GroupList = None
        self.SubscribeList = None

    def SendMessageToFriend(self):
        pass

    def GetFriendList(self):
        if not self.FriendList:
            self.FriendList = self.bot.friends()

    def GetGroupList(self):
        if not self.GroupList:
            self.GroupList = self.bot.groups()

    def GetSubscribeList(self):
        if not self.SubscribeList:
            self.SubscribeList = self.bot.mps()

    def StartListening(self):
        embed()


class Recorder():
    def __init__(self, UserName, HistoryFileLocation):
        self.Wechat = WechatWraper(fjoin(HistoryFileLocation, UserName, 'WechatLoginProfile'))
        self.StartTime = Date() 
        self.UserName = UserName
        self.HistoryFileLocation = HistoryFileLocation
        self.Chat = []

    def StartRecording(self):
        @self.Wechat.MessageHandler(except_self=False)
        def handler(msg):
            try:
                print('---------------start-----------------')
                if (type(msg.sender) == Group):
                    print('From: ' + str(msg.sender) + ' : ' + str(msg.member))
                else:
                    print('From: ' + str(msg.sender))
                print('To: ' + str(msg.receiver))
                print('Message:  ' + str(msg.type) + ' : ' + str(msg.text))
                if msg.type == 'Sharing':
                    print('url: ' + str(msg.url))
                print('\n')
            except Exception as e:
                print(e)
        self.Wechat.StartListening()

    def __del__(self):
        pass

class Historian():
    def __init__(self):
        pass