import PyBear.GlobalBear as GlobalBear
import PyBear.Library.WebSuite as WebSuiteBear

def GetHandler(Client):
    Client.Redirect('''https://www.baidu.com/s?wd=%s'''%(Client.Argument['q'][0].decode('utf-8')))

WebSuiteBear.StartHttpsServer(GlobalBear.Location('DefaultCertificationFileLocation'), GetHandler=GetHandler, Port=GlobalBear.DefaultBearSearchPort)