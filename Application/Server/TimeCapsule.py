import PyBear.GlobalBear as GlobalBear
import PyBear.Library.WebSuite as WebSuiteBear
import PyBear.Tool.TimeCapsule as TimeCapsuleBear

def ParameterAnalyst(Request, Argument, Body):
    print([Request, Argument, Body])
    pass

def PostHandler(Client):
    pass 

WebSuiteBear.StartHttpServer(PostHandler=PostHandler, ParameterAnalyst=ParameterAnalyst, Port=GlobalBear.TimeCapsulePort)