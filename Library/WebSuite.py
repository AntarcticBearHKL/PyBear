from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import requests
import os,sys
import json
import ssl
import re

from PyBear.GlobalBear import *
from PyBear.Library.Data.File import *

def StartHttpServer(ApplicationFileLocation=None, LibraryFileLocation=None, GetHandler=None, PostHandler=None, Port=80):
    Application( [(r".*", GetHttpServerListener(ApplicationFileLocation, LibraryFileLocation, GetHandler, PostHandler) ),] ).listen(Port)
    IOLoop.instance().start()

def StartHttpsServer(CertificationFileLocation, ApplicationFileLocation=None, LibraryFileLocation=None, GetHandler=None, PostHandler=None, Port=443):
    HTTPServer(
        Application(
            [(r".*", GetHttpServerListener(ApplicationFileLocation, LibraryFileLocation, GetHandler, PostHandler)),], 
            **{
            "static_path" : FJoin(os.path.dirname(__file__), "static"),
        }),
        ssl_options={
            "certfile": FJoin(CertificationFileLocation, 'server.crt'),
            "keyfile": FJoin(CertificationFileLocation, 'server.key'),
        }).listen(Port)
    IOLoop.instance().start()

def GetHttpServerListener(ApplicationFileLocation, LibraryFileLocation, GetHandler, PostHandler):
    class HTTPListener(RequestHandler):
        def get(self):
            try:
                if GetHandler:
                    GetHandler(RequestAnalyst(self, ApplicationFileLocation, LibraryFileLocation))
            except Exception as Error:
                print(Error)
                self.set_status(403)
                self.write('Nobody Want To Respond You')

        def post(self):
            try:
                if PostHandler:
                    PostHandler(RequestAnalyst(self, ApplicationFileLocation, LibraryFileLocation))   
            except Exception as Error:
                print(Error)
                self.set_status(403)
                self.write('Nobody Want To Respond You')
    return HTTPListener


class RequestAnalyst:
    def __init__(self, Connection, ApplicationFileLocation, LibraryFileLocation):
        self.Connection = Connection
        self.Parameter = {}

        self.ApplicationFileLocation = ApplicationFileLocation
        self.LibraryFileLocation = LibraryFileLocation
        self.Method = self.Connection.request.method
        self.Path = self.Connection.request.path.split('/')

        self.DefaultApplication = None
        self.ErrorApplication = None

        try:
            if self.Path[1] == '':
                if self.DefaultApplication:
                    self.Path = ['', self.DefaultApplication, 'html', 'index.html']
                elif self.ErrorApplication:
                    self.Path = ['', self.ErrorApplication, 'html', 'index.html']
                else:
                    self.Path = None
            elif len(self.Path) == 2:
                self.Path += ['html', 'index.html']
        except Exception as Error:
            print(Error)
            print('Get Path Error')    

        self.Request = self.Connection.request
        self.Argument = self.Connection.request.arguments
        self.Body = self.Connection.request.body


    def Write(self, Content):
        self.Connection.write(Content)

    def PrintRequest(self):
        for Item in self.Request.__dict__:
            print(i, ':', self.Request.__dict__[i])

    def ReturnApplicationGet(self):
        if not self.Path:
            raise BadBear('No Application Selected')
        RetFile = FBRead(self.GetFilePath())
        Filetype = self.Path[2]
        if Filetype == 'html':
            self.Connection.set_header('Content-Type', 'text/html')
        elif Filetype == 'css' or Filetype == 'libcss':
            self.Connection.set_header('Content-Type', 'text/css')    
        elif Filetype == 'javascript' or Filetype == 'libjs':
            self.Connection.set_header('Content-Type', 'text/javascript')
        else:
            self.Connection.set_header('Content-Type', 'application/octet-stream')
        self.Connection.write(RetFile)

    def ReturnApplicationPost(self):
        if self.GetApplication() in FList(self.ApplicationFileLocation):
            APIFileLocation = FJoin(self.ApplicationFileLocation, self.GetApplication())
            sys.path.append(APIFileLocation)
            exec('import ' + self.GetApplication() + '_api.py')
            exec(self.GetApplication()+'_api.Handler()')
        else:
            raise BadBear('Application Not Found')


    def SetDefaultApplication(self, DefaultApplication):
        self.DefaultApplication = DefaultApplication

    def SetErrorApplication(self, ErrorApplication):
        self.ErrorApplication = ErrorApplication

 
    def GetMethod(self):
        return self.Method

    def GetParameter(self):
        return self.Parameter

    def GetApplication(self): 
        if len(self.Path) > 1:
            return self.Path[1]
        else:
            return self.DefaultPage

    def GetFilePath(self):
        if self.Path[2] == 'libcss' or self.Path[2] == 'libjs':
            FilePath = self.LibraryFileLocation
            for Item in self.Path[3:]:
                FilePath = FJoin(FilePath, Item)
        else:
            FilePath = FJoin(self.ApplicationFileLocation, self.Path[1])
            for Item in self.Path[2:]:
                FilePath = FJoin(FilePath, Item)
        return FilePath

    def Redirect(self, Destination):
        self.Connection.redirect(Destination)



def StartSocketServer():
    pass

def SendHttpGet(Url, Parameter):
    Request = requests.get(Url+'?'+Parameter)
    return [Request.status_code, Request.text]

def SendHttpPost(Url, Parameter):
    Request = requests.post(Url, data=json.dumps(Parameter))
    return [Request.status_code, Request.text]

def SendTcpRequest():
    pass

def SendUdpRequest():
    pass



def GetPrivateIP():
    Request = requests.get("http://www.baidu.com", stream=True)
    IP = Request.raw._connection.sock.getsockname()
    return IP[0]

def GetPublicIP():
    Request = requests.get("http://www.net.cn/static/customercare/yourip.asp")
    IP = re.findall(r'\d+\.\d+\.\d+\.\d+', Request.content.decode('utf-8', errors='ignore'))
    return IP[0]