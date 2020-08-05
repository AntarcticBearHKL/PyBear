import json

import PyBear.GlobalBear as GlobalBear
import PyBear.Library.WebSuite as WebSuiteBear
import PyBear.Tool.TimeCapsule as TimeCapsuleBear

def PostHandler(Client):
    Command = Client.Parameter['Command']
    if Command in ['DairyBook','NoteBook','Contact','Balance','File']:
        exec(Client.Parameter['Command']+'(Client)')
    else:
        print('Command Error')

def ParameterAnalyst(Request, Argument, Body):
    Ret = {}
    Ret['Command'] = Argument['Command'][0].decode('utf-8')
    ClientBody = json.loads(Body.decode('utf-8'))
    for Item in ClientBody:
        Ret[Item] = ClientBody[Item]
    return Ret

def DairyBook(Client):
    print(Client.Parameter)
    TimeCapsuleBear.DairyBook().NewEvent(Client['Content'])

WebSuiteBear.StartHttpsServer(GlobalBear.Location('DefaultCertificationFileLocation'), PostHandler=PostHandler, ParameterAnalyst=ParameterAnalyst)