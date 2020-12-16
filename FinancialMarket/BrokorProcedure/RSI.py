import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self, Brokor):
        Brokor.RequireData(['Close'])
        RSIF = talib.RSI(numpy.array(Brokor.GetData('Close')), timeperiod=5)
        RSIS = talib.RSI(numpy.array(Brokor.GetData('Close')), timeperiod=22)
        RSI = RSIF-RSIS+50

        Brokor.ProvideData({
            'RSIF': RSIF,
            'RSIS': RSIS,
            'RSI': RSI})