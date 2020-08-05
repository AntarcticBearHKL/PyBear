#! coding=utf-8
import os, sys
import json

from BearPY import Config
from BearPY.libraries.Debug import *
from BearPY.libraries.Data.MySQL import *

from BearPY.tools.Authentication import *

def handler(request, client):
    clientCommand = client.parameter['command']
    clientParameter = json.loads(client.parameter['parameter'])
    if clientCommand == 'signUp':
        request.write(str(signUP(clientParameter['username'], clientParameter['password'])))
    elif clientCommand == 'login':
        result = str(login(clientParameter['username'], clientParameter['password']))
        request.set_cookie('auid', result)
        request.write(result)    