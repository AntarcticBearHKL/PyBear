from BearPY import GlobalBear

if GlobalBear.GlobalAvailabilityCheck:
    print('--------------- Global Availability Check Start ---------------')
    from BearPY.Libraries.CLib import *

    from BearPY.Libraries.Data.CSV import *
    from BearPY.Libraries.Data.DataFrame import *
    from BearPY.Libraries.Data.Excle import *
    from BearPY.Libraries.Data.File import *
    from BearPY.Libraries.Data.LogicSequence import *
    from BearPY.Libraries.Data.MySQL import *
    from BearPY.Libraries.Data.TimeSequence import *
    from BearPY.Libraries.Data.WebDisk import *
    from BearPY.Libraries.Data.Word import *

    from BearPY.Libraries.DeepLearning import *
    from BearPY.Libraries.Financial import *
    from BearPY.Libraries.InputCheck import *
    from BearPY.Libraries.Language import *
    from BearPY.Libraries.MachineLearning import *
    from BearPY.Libraries.Math import *
    from BearPY.Libraries.Matrix import *
    from BearPY.Libraries.Multitasks import *
    from BearPY.Libraries.NLP import *
    from BearPY.Libraries.RegularExpression import *
    from BearPY.Libraries.Statistics import *

    from BearPY.Tools.Authentication import *
    from BearPY.Tools.FinancialMarket import *
    from BearPY.Tools.Wechat import *
    from BearPY.Tools.WechatSubscribeBackend import *
    print('--------------- Global Availability Check Successful ---------------')