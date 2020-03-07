import os, sys

from PyBear.GlobalBear import *
from PyBear.Library.Time import *
from PyBear.Library.Data.File import *

WebDiskFileLocation = {}
def NewWebDiskFileLocation(Name, Dir):
    WebDiskFileLocation[Name] = Dir

WebDiskFileLocation = {}
def NewWebDiskFileLocation(Name, Dir):
    WebDiskFileLocation[Name] = Dir

class WebDisk():
    def __init__(self, diskname, application, username, url='/', admin=False):
        self.diskname = diskname
        self.application = application
        self.username = username
        self.url = str(url).split('/')[1:]
        self.getPath()
        self.getNodes()

    def GetPath(self):
        self.path = fjoin(Config.WebDiskConfig[self.diskname], self.application, self.username)
        for item in self.url:
            self.path = fjoin(self.path, item)

    def GetNodes(self):
        self.nodes = flist_pro(self.path)

    def List(self):
        return self.nodes

    def NewFile(self, name, content):
        if self.exist(name):
            return WD_Node_Exists
        fbwrite(fjoin(self.path, name), content)

    def NewDirectory(self, name):
        if self.exist(name):
            return WD_Node_Exists
        fmkdir(fjoin(self.path, name))

    def ChangeName(self, old, new):
        if self.exist(name):
            return WD_Node_Exists
        frename(fjoin(self.path, old), fjoin(self.path, new))

    def MoveNode(self):
        if self.exist(name):
            return WD_Node_Exists

    def DeleteNode(self, name):
        if self.exist(name):
            return WD_Node_Exists
        if fisfile(fjoin(self.path, name)):
            frmfile(fjoin(self.path, name))
        elif fisdir(fjoin(self.path, name)):
            frmdir(fjoin(self.path, name))

    def GetProperities(self,  name):
        if self.exist(name):
            filetype = self.nodes[name]
            changetime = Date(os.path.getmtime(fjoin(self.path, name))).to_string(style='L1')
            filesize = os.path.getsize(fjoin(self.path, name))
            if filesize > 1000:
                filesize = str(round(filesize/1000, 2)) + 'KB'
            elif filesize > 1000000:
                filesize = str(round(filesize/1000000, 2)) + 'MB'
            elif filesize > 1000000000:
                filesize = str(round(filesize/1000000000, 2)) + 'GB'
            else:
                filesize = str(filesize) + 'B'
            return [filetype, filesize, changetime]
        else:
            return WD_Node_Not_Exists

    def CountFile(self):
        return len([item for item in self.nodes if self.nodes[item]=='file'])

    def CountDirectory(self):
        return len([item for item in self.nodes if self.nodes[item]=='directory'])

    def Exist(self, name, filetype=None):
        if name in self.nodes.keys():
            if filetype:
                if self.nodes[name] == filetype:
                    return True
                return False
            return True
        return False