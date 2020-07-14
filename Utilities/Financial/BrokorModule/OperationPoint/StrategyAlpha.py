import talib
import numpy

import PyBear.GlobalBear as GlobalBear

class Config:
    def Run(self, Brokor):
        Brokor.Result['StrategyAlpha'] = Brokor.GetEmptyList()
        Brokor.Traversal(self.TraversalFunction, LeftMargin=2)
        
    def TraversalFunction(self, b):
        ConditionA = b.j([
            [
                b.g('DIF', -1) < 0,
                b.g('DIF', 0) > 0,
                b.g('DEA', 0) < 0,
                b.g('DEA', 0) < b.g('DIF', 0),
                b.g('DEA', -1) < b.g('DIF', -1),
                b.g('KDJ', 0) > 80,
                b.g('RSI', 0) > 70,
            ],
        ])
        ConditionB = b.j([
            [
                b.g('DIF', 0) > 0,
                b.g('DEA', 0) > 0,
                b.g('DIF', 0) > b.g('DEA', 0),
                b.g('KDJ', 0) > 80,
                b.g('RSI', 0) > 67,
                b.g('RSI', -1) < 65,
                b.g('MACD', -1) < b.g('MACD', 0),
            ],
        ])
        if ConditionA:
            b.Result['StrategyAlpha'].append([1])
        if ConditionB:
            b.Result['StrategyAlpha'].append([2])
        else:
            b.Result['StrategyAlpha'].append(None)