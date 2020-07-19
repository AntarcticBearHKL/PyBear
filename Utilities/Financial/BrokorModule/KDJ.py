import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorModule):
    def Run(self, Brokor):
        Brokor.RequireData(['High', 'Low', 'Close'])
        K, D = talib.STOCH(
            numpy.array(Brokor.GetData('High')),
            numpy.array(Brokor.GetData('Low')),
            numpy.array(Brokor.GetData('Close')),
            fastk_period = 22,
            slowk_period = 5,
            slowk_matype = 0,
            slowd_period = 5,
            slowd_matype = 0,)
        J = K - D + 50

        Brokor.ProvideData({
            'KDJF': K,
            'KDJS': D,
            'KDJ': J,})