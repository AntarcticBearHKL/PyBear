import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear

class Analyst:
    def __init__(self):
        self.ModuleList = []
        self.PortfolioList = []

    def LoadModule(self, Module):
        self.ModuleList.append(Module)

    def Run(self):
        for Module in self.ModuleList:
            Module.Run()
            self.PortfolioList.append(Module.Portfolio)
        for Portfolio in self.PortfolioList:
            Portfolio()


class AnalystProcedure:
    def Run(self):
        pass
    
    def Portfolio(self):
        pass