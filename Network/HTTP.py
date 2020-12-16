from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import requests
import os,sys
import json
import ssl
import re

import PyBear.Bear as Bear
import PyBear.System.File as File

def HttpServer(
    PageLocation=None, LibraryLocation=None, 
    GetHandler=None, PostHandler=None, ParameterAnalyst=None, Port=80):
    Application( [(r".*", GetHttpServerListener(PageLocation, LibraryLocation, GetHandler, PostHandler, ParameterAnalyst) ),] ).listen(Port)
    IOLoop.instance().start()

def HttpsServer(
    CertificationLocation, PageLocation=None, LibraryLocation=None, 
    GetHandler=None, PostHandler=None, ParameterAnalyst=None, Port=443):
    HTTPServer(
        Application(
            [(r".*", GetHttpServerListener(PageLocation, LibraryLocation, GetHandler, PostHandler, ParameterAnalyst)),], 
            **{
            "static_path" : File.Join(os.path.dirname(__file__), "static"),
        }),
        ssl_options={
            "certfile": File.Join(CertificationLocation, 'crt'),
            "keyfile": File.Join(CertificationLocation, 'key'),
        }).listen(Port)
    IOLoop.instance().start()

def GetHttpServerListener(PageLocation, LibraryLocation, 
    GetHandler, PostHandler, ParameterAnalyst):
    class HTTPListener(RequestHandler):
        def get(self):
            try:
                if GetHandler:
                    GetHandler(RequestAnalyst(self, PageLocation, LibraryLocation, ParameterAnalyst))
            except Exception as Error:
                print(Error)
                self.set_status(403)
                self.write('Nobody Want To Respond You')

        def post(self):
            try:
                if PostHandler:
                    PostHandler(RequestAnalyst(self, PageLocation, LibraryLocation, ParameterAnalyst))   
            except Exception as Error:
                print(Error)
                self.set_status(403)
                self.write(' Nobody Responds You ')
    return HTTPListener


class RequestAnalyst:
    def __init__(self, Connection, PageLocation, LibraryLocation, ParameterAnalyst):
        self.Connection = Connection

        self.PageLocation = PageLocation
        self.LibraryLocation = LibraryLocation
        self.Method = self.Connection.request.method
        self.Path = self.Connection.request.path.split('/')

        self.Request = self.Connection.request
        self.Argument = self.Connection.request.arguments
        self.Body = self.Connection.request.body

        if ParameterAnalyst:
            self.Parameter = ParameterAnalyst(self.Request, self.Argument, self.Body)
        else:
            self.Parameter = {}


    def Write(self, Content):
        self.Connection.write(Content)


    def ReturnPage(self):
        Filetype = self.Path[1]

        if len(self.Path)==1 or Filetype == '':
            self.Connection.write('URL ERROR')

        if Filetype == 'libcss' or Filetype == 'libjs':
            FilePath = self.LibraryLocation
        else:
            FilePath = File.Join(self.PageLocation, Filetype)

        for Item in self.Path[2:]:
            FilePath = File.Join(FilePath, Item)

        RetFile = File.ReadB(FilePath)

        if Filetype == 'html':
            self.Connection.set_header('Content-Type', 'text/html')
        elif Filetype == 'css' or Filetype == 'libcss':
            self.Connection.set_header('Content-Type', 'text/css')    
        elif Filetype == 'javascript' or Filetype == 'libjs':
            self.Connection.set_header('Content-Type', 'text/javascript')
        else:
            self.Connection.set_header('Content-Type', 'application/octet-stream')

        self.Connection.write(RetFile)


    def Redirect(self, Destination):
        self.Connection.redirect(Destination)


    def GetCookie(self):
        pass

    def SetCookie(self):
        pass


    def PrintRequest(self):
        for Item in self.Request.__dict__:
            print(Item, ':', self.Request.__dict__[Item])
        print('---------------------------------------')
        for Item in self.__dict__:
            print(Item, ':', self.__dict__[Item])
        print('---------------------------------------')



def GetPrivateIP():
    Request = requests.get("http://www.baidu.com", stream=True)
    IP = Request.raw._connection.sock.getsockname()
    return IP[0]

def GetPublicIP():
    Request = requests.get("http://www.net.cn/static/customercare/yourip.asp")
    IP = re.findall(r'\d+\.\d+\.\d+\.\d+', Request.content.decode('utf-8', errors='ignore'))
    return IP[0]