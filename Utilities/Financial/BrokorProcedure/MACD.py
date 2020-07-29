import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        DIF, DEA, MACD = talib.MACD(
            numpy.array(self.Input('Close')),
            fastperiod=self.GetConfigInt('Fast', '5'), 
            slowperiod=self.GetConfigInt('Slow', '22'), 
            signalperiod=self.GetConfigInt('Signal', '9'))
        MACD = MACD*2

        MACDV = [numpy.NaN]
        for Count in range(len(MACD)-1):
            MACDV.append(MACD[Count+1]-MACD[Count])

        MACDV = talib.MA(
            numpy.array(MACDV),
            timeperiod=5,
        )

        self.Output('DIF', DIF)
        self.Output('DEA', DEA)
        self.Output('MACD', MACD*2)
        self.Output('MACDV', MACDV)

        self.LeftMargin = 2
        self.Brokor.NewEmptyList('MACDX', self.LeftMargin)
        self.Brokor.NewEmptyList('MACDVX', self.LeftMargin)

    def TraversalFunction(self, b):
        ConditionA = b.j([
            [
                b.d('MACD', -2) < 0,
                b.d('MACD', -1) > 0,
            ],
        ])
        ConditionB = b.j([
            [
                b.d('MACD', -2) > 0,
                b.d('MACD', -1) < 0,
            ],
        ])
        if ConditionA:
            b.Data['MACDX'].append(1)
        elif ConditionB:
            b.Data['MACDX'].append(-1)
        else:
            b.Data['MACDX'].append(0)

        ConditionA = b.j([
            [
                b.d('MACDV', -2) < 0,
                b.d('MACDV', -1) > 0,
            ],
        ])
        ConditionB = b.j([
            [
                b.d('MACDV', -2) > 0,
                b.d('MACDV', -1) < 0,
            ],
        ])
        if ConditionA:
            b.Data['MACDVX'].append(1)
        elif ConditionB:
            b.Data['MACDVX'].append(-1)
        else:
            b.Data['MACDVX'].append(0)