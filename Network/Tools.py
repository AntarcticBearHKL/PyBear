import requests

import PyBear.Bear as Bear

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