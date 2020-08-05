import json

from BearPY import Config
from BearPY.libraries.Debug import *

from BearPY.tools.Authentication import *
from BearPY.tools.WebDisk import *

def handler(request, client):
    if 'Command' in client.parameter:
        exec(client.parameter['Command'] + '(request, client)')
    elif request.request.body_arguments['Command'][0].decode('ascii') == 'Upload':
        upload(request, client)

def Login(request, client):
    username = authentication(request.get_cookie('auid'))
    request.write(username)

def ListDir(request, client):
    username = authentication(request.get_cookie('auid'))
    wd = WebDisk('default', 'WebDisk', username, url = client.parameter['Url'])
    ret = {}
    for item in wd.listNodes():
        ret[item] = wd.getProperities(item)
    request.write(json.dumps(ret))

def NewDir(request, client):
    username = authentication(request.get_cookie('auid'))
    wd = WebDisk('default', 'WebDisk', username, url = client.parameter['Url'])
    wd.newDirectoryNode(client.parameter['DirectoryName'])

def Move(request, client):
    pass

def ChangeName(request, client):
    pass

def DeleteFile(request, client):
    pass

def Upload(request, client):
    username = authentication(request.get_cookie('auid'))

    wd = WebDisk('default', 'WebDisk', username, url = request.request.body_arguments['Url'][0].decode('ascii'))

    wd.newFileNode(request.request.files['file'][0]['filename'],
    request.request.files['file'][0]['body'])