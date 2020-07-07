import talib
import numpy

import PyBear.GlobalBear as GlobalBear

class Config:
    def Run(self, Brokor):
        Brokor.Result['StrategyAlpha'] = Brokor.GetEmptyList()
        Brokor.Traversal(self.TraversalFunction, LeftMargin=2)
        
    def TraversalFunction(self, b):
        C1 = b.j([
            b.g('DIF', -1)<0,
            b.g('DIF', 0)>0,
            b.g('DEA', 0)<0,
            b.g('DEA', 0)<b.g('DIF', 0),
            b.g('DEA', -1)<b.g('DIF', -1),
            b.g('MACD', 0)>0,
            b.g('Close', 0)<b.g('BOLLUpper', 0),
            b.g('KDJ', 0)>50,
            b.g('RSI', 0)>50,
        ])
        if C1:
            ProfitP = (b.g('Close',0)-b.g('Close',-1))/b.g('Close',-1)
            b.Result['StrategyAlpha'].append([ProfitP])
        else:
            b.Result['StrategyAlpha'].append(None)