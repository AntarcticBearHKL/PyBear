import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorModule):
    def Run(self, Brokor):
        self.LeftMargin = 1
        Brokor.Data['StrategyAlpha'] = [None] * self.LeftMargin
        Brokor.Result['StrategyAlpha'] = []
        
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
            b.r['StrategyAlpha'].append(b.d())
        if ConditionB:
            b.Data['StrategyAlpha'].append(2)
            b.r['StrategyAlpha'].append(b.d())
        else:
            b.Data['StrategyAlpha'].append(None)