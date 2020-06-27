import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear

class Analyst:
    def __init__(self):
        self.ModuleList = []

    def LoadModule(self, Module):
        self.ModuleList.append(Module)

    def Run(self):
        for Module in self.ModuleList:
            Module.Module.Run()

class AnalystModule:
    def __init__(self):
        pass

    def Run(self):
        pass