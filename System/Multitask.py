import multiprocessing
import threading
import os,sys
import time

import PyBear.Bear as GlobalBear
import PyBear.System.Chronus as ChronusBear
import PyBear.DataBase.Redis as RedisBear

class SimpleThread:
    def __init__(self, Function, Argc):
        self.Function = Function
        self.Argc = Argc
    
    def Start(self):
        threading.Thread(target = self.Function, args = self.Argc).start()

class MultThread:
    def __init__(self, ParallelNumber, LimitPerMinute = None):
        self.TaskList = []
        self.ParallelNumber = ParallelNumber
        self.LimitPerMinute = LimitPerMinute

    def ImportTask(self, Function, TaskArg):
        for Item in TaskArg:
            self.TaskList.append([Function, tuple(Item)])

    def SetTask(self, TaskList):
        self.TaskList = TaskList

    def Start(self):
        WorkSpace = []
        for Item in range(self.ParallelNumber):
            WorkSpace.append(None)

        LimitTimer = ChronusBear.Date()
        LimitCounter = 0

        for Task in self.TaskList:
            #print(LimitCounter)
            if self.LimitPerMinute and LimitCounter >= self.LimitPerMinute:
                while(True):
                    if (ChronusBear.Date() - LimitTimer) > 60:
                        LimitTimer = ChronusBear.Date()
                        LimitCounter = 0
                        break
                    print('Waiting')
                    ChronusBear.Chronus.Sleep(1)
            LimitCounter += 1

            CONTINUE = True
            AvailableThread = None

            while(CONTINUE):
                for Item in range(self.ParallelNumber):
                    if (WorkSpace[Item] == None) or (WorkSpace[Item].isAlive() == False):
                        CONTINUE = False
                        AvailableThread = Item
                        break
                    
            WorkSpace[AvailableThread] = threading.Thread(target = Task[0], args = Task[1])
            #RedisBear.Redis('RedisLocal').hset('Multitask', str(AvailableThread), ' '.join([str(Item) for Item in Task[1]]) + ChronusBear.Date().String(2))
            WorkSpace[AvailableThread].start() 

        for Item in WorkSpace:
            if Item != None:
                Item.join() 


class MultCore:
    def __init__(self, ParallelNumber):
        self.TaskList = []
        self.ParallelNumber = ParallelNumber

    def ImportTask(self, Function, TaskArg):
        for Item in TaskArg:
            self.TaskList.append([Function, tuple(Item)])

    def SetTask(self, TaskList):
        self.TaskList = TaskList

    def Start(self): 
        WorkSpace = []
        for Item in range(self.ParallelNumber):
            WorkSpace.append(None)

        for Task in self.TaskList:
            CONTINUE = True
            AvailableThread = None

            while(CONTINUE):
                for Item in range(self.ParallelNumber):
                    if (WorkSpace[Item] == None) or (WorkSpace[Item].is_alive() == False):
                        CONTINUE = False
                        AvailableThread = Item
                        break
                    
            WorkSpace[AvailableThread] = multiprocessing.Process(target = Task[0], args = Task[1])
            WorkSpace[AvailableThread].start() 

        for Item in WorkSpace:
            if Item != None:
                Item.join() 


class TaskMatrix:
    def __init__(self, Core, Thread, LimitPerMinute = None):
        self.Core = Core
        self.Thread = Thread
        self.TaskList = []
        self.LimitPerMinute = LimitPerMinute

        for Item in range(self.Core):
            self.TaskList.append([])
        self.AutoArrangedTaskList = []

    def ImportTask(self, Function, TaskArg):
        for Item in TaskArg:
            self.AutoArrangedTaskList.append([Function, tuple(Item)])

    def NewProcess(self, ProcessTaskArg):
        MultThreadProcess = MultThread(self.Thread, LimitPerMinute = self.LimitPerMinute)
        MultThreadProcess.SetTask(ProcessTaskArg)
        MultThreadProcess.Start()

    def Start(self):
        TaskPointer = 0
        Corepointer = 0
        TaskNumber = len(self.AutoArrangedTaskList)
        while(TaskPointer<TaskNumber):
            self.TaskList[Corepointer].append(self.AutoArrangedTaskList[TaskPointer])
            TaskPointer += 1
            Corepointer += 1
            if Corepointer == self.Core:
                Corepointer = 0

        MultiCoreProcess = MultCore(self.Core)
        TaskArg = [[self.TaskList[Item]] for Item in range(self.Core)]
        MultiCoreProcess.ImportTask(self.NewProcess, TaskArg)

        MultiCoreProcess.Start()