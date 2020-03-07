import json

from PyBear.GlobalBear import *
from PyBear.Library.RegularExpression import *
from PyBear.Library.Data.File import *

class LogicSequence:
    def __init__(self, baseName, name):
        self.Name = name
        self.BaseName = baseName
        self.FullName = fjoin(baseName, name)
        if not self.load():
            self.Content = {
                'equivalency':[], 
                'analogue':{}, 
                'have':[],
                'Property':{}}
            self.save()

    def load(self):
        if fexists(self.FullName):
            self.Content = json.loads(fread(self.FullName))
            for item in self.Content['Property']:
                if recontain(self.Content['Property'][item], '_t_'):
                    self.Content['Property'][item] = TimeSequence(self.BaseName, name)
            return True
        return False

    def save(self):
        _temp = self.Content
        for item in _temp['Property']:
                if (self.Content['Property'][item]) == 'TimeSequence':
                    self.Content['Property'][item] = '_t_' + self.Name
        fuwrite(self.FullName, json.dumps(_temp))

    def defineProperty(self, a, b):
        self.Content['Property'][a] = b
        self.save()

    def defineEquivalency(self, b):
        if b not in self.Content['equivalency']:
            self.Content['equivalency'].append(b)
        self.save()

    def defineAnalogue(self, a, p):
        self.Content['analogue'][a] = b
        self.save()

    def defineHave(self, b):
        if b not in self.Content['have']:
            self.Content['have'].append(b)
        self.save()

    def __getitem__(self, item = 'have'):
        return self.Content[item]
            
def logicStrongLink(baseName, a, b):
    LogicSequence(baseName, a).defineEquivalency(b)
    LogicSequence(baseName, b).defineEquivalency(a)

def logicWeakLink(baseName, a, b, pab, pba):
    LogicSequence(baseName, a).defineAnalogue(b, pab)
    LogicSequence(baseName, b).defineAnalogue(a, pba)