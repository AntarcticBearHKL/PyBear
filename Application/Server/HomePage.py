from BearPY.GlobalBear import *
from BearPY.Libraries.WebSuite import *
from BearPY.Libraries.Data.File import *

ApplicationFileLocation='E:\GitHub\BearApplication\PythonApplication\Applications\ServerApplication'
LibraryFileLocation='E:\GitHub\BearApplication\PythonApplication\Applications\ServerLibrary'

def GetHandler(Connect):
    Connect.ReturnApplication()

def PostHandler(Connect):
    Connect.HandlePost()

StartHttpServer(ApplicationFileLocation, LibraryFileLocation, GetHandler=GetHandler, PostHandler=PostHandler)