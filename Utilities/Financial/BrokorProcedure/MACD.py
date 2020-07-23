import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self, Brokor):
        Brokor.RequireData(['Close'])
        DIF, DEA, MACD = talib.MACD(
            numpy.array(Brokor.GetData('Close')),
            fastperiod=5, 
            slowperiod=22, 
            signalperiod=9)

        Brokor.ProvideData({
            'DIF': DIF,
            'DEA': DEA,
            'MACD': MACD*2,})