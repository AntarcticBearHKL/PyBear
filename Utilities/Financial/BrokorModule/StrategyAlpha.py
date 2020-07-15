import talib
import numpy

import PyBear.GlobalBear as GlobalBear

class Config:
    def Run(self, Brokor):
        LeftMargin = 1
        Brokor.Data['StrategyAlpha'] = [None] * LeftMargin
        Brokor.Traversal(self.TraversalFunction, LeftMargin=LeftMargin)
        
    def TraversalFunction(self, b):
        ConditionA = b.j([
            [
                b.g('DIF', -1) < 0,
                b.g('DIF', 0) > 0,
                b.g('DEA', -1) < 0,
                b.g('DEA', 0) < 0,
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
            b.Data['StrategyAlpha'].append(1)
        if ConditionB:
            b.Data['StrategyAlpha'].append(2)
        else:
            b.Data['StrategyAlpha'].append(None)