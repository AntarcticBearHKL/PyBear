import PyBear.GlobalBear as GlobalBear

if GlobalBear.GlobalTestModuleOn:
    print('--------------- Global Availability Check Start ---------------')
    
    import PyBear.Library.Automation as AutomationBear
    import PyBear.Library.Chart as ChartBear
    import PyBear.Library.Chronus as ChronusBear
    import PyBear.Library.Cipher as CipherBear
    import PyBear.Library.CLib as CLibBear
    import PyBear.Library.DeepLearning as DeepLearningBear
    import PyBear.Library.Financial as FinancialBear
    import PyBear.Library.MachineLearning as MachineLearningBear
    import PyBear.Library.Math as MathBear
    import PyBear.Library.ModuleManager as ModuleManagerBear
    import PyBear.Library.Multitasks as MultitasksBear
    import PyBear.Library.NLP as NLPBear
    import PyBear.Library.Statistics as StatisticsBear
    import PyBear.Library.WebSuite as WebSuiteBear
    import PyBear.Library.Wechat as WechatBear

    import PyBear.Library.Data.CSV as CSVBear
    import PyBear.Library.Data.Excle as ExcleBear
    import PyBear.Library.Data.File as FileBear
    import PyBear.Library.Data.MongoDB as MongoBear
    import PyBear.Library.Data.MySQL as MySQLBear
    import PyBear.Library.Data.Redis as RedisBear
    import PyBear.Library.Data.WebDisk as WebDiskBear
    import PyBear.Library.Data.Word as WordBear

    import PyBear.Tool.Authentication as AuthenticationBear
    import PyBear.Tool.Balance as BalanceBear
    import PyBear.Tool.Contact as ContactBear
    import PyBear.Tool.FinancialMarket as FinancialMarketBear
    import PyBear.Tool.NoteBook as NoteBookBear
    import PyBear.Tool.TimeCapsule as TimeCapsuleBear

    print('--------------- Global Availability Check Successful ---------------')