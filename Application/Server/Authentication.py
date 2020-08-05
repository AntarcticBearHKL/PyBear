from PyBear.GlobalBear import *
from PyBear.Library.WebSuite import *
from PyBear.Library.Data.MySQL import *

def PostHandler(Connect):
    pass


StartHttpServer(PostHandler=PostHandler, Port=6210) 