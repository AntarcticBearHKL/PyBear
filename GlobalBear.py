DebugMode = False
GlobalAvailabilityCheck = False

Results = {}
ResultCode = {}

class Result:
    def __init__(self, *args):
        if args[0] in ResultCode:
            self.Value = ResultCode[args[0]][0]
            self.Explain = ResultCode[args[0]][1]
            self.HandlerFunction = ResultCode[args[0]][2]
        else:
            self.Value = args[0]
            self.Explain = args[1]
            self.HandlerFunction = DefaultResultHandlerFunction
        self.Result = self.Value

    def __str__(self):
        return self.Explain
    
    def ResultWithHandler(self, *args):
        if len(args)==1:
            exec('Results[\'' + str(args[0]) + '\'] = self')
        self.HandlerFunction()
        return self.Value

    def ResultWithDebug(self):
        if DebugMode:
            print('Return Value: ' + self.Value)
            print('Return Explain: ' + self.Explain)
            FunctionReturn = self.HandlerFunction()
            print('HandlerFunction Return: ' + FunctionReturn)
        return self.Value

def ResultWithFunction(Value, Explain):
    def RetFunction(Function):
        Results[Explain] = [Value, Explain, Function]
    return RetFunction

def DefaultResultHandlerFunction():
    print('No Result Handler Function Defined')


class BadBear(Exception):
    def __init__(self, Explain):
        self.Explain = Explain
    
    def __str__(self):
        return '----------------Error Happend----------------\n' + self.Explain