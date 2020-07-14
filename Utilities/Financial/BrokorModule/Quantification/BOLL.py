import talib
import numpy

import PyBear.GlobalBear as GlobalBear

class Config:
    def Run(self, Brokor):
        Brokor.RequireData(['Open', 'Close'])
        Open = numpy.array(Brokor.GetData('Open'))
        Close = numpy.array(Brokor.GetData('Close'))
        Upper, Mid, Lower = talib.BBANDS((Open+Close)/2, timeperiod=22)

        Brokor.ProvideData({
            'BOLLUpper': Upper,
            'BOLLMid': Mid,
            'BOLLLower': Lower,})