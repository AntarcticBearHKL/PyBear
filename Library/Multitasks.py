import multiprocessing
import threading
import os,sys
import time

from PyBear.GlobalBear import *
from PyBear.Library.Chronus import *

class ThreadPool:
    def __init__(self, Mode, Limit=None, Timer=False, Progress=False):
        self.TaskList = []
        self.Mode = Mode

        self.Limit = Limit
        self.Timer = Timer
        self.Progress = Progress

    def NewTask(self, Function, Arguments):
        self.TaskList.append([Function, tuple(Arguments)])

    def NewTasks(self, Group, Function, Arguments):
        for Item in Group:
            self.TaskList.append([Function, tuple([Item]+Arguments)])


    def Start(self, ParallelNumber):
        StartTime = time.time()
        WorkSpace = []
        for Item in range(ParallelNumber):
            WorkSpace.append(None)

        ProgressCounter = 0
        FinishLine = len(self.TaskList)

        LimitCounter = 0
        LimitTimer = Date()

        for Task in self.TaskList:
            if self.Progress:
                ProgressCounter += 1
                print('='* 80 +str(round(ProgressCounter*100/ FinishLine, 2))+ '%')

            CONTINUE = True
            AvailableThread = None

            if self.Limit:
                print('nnn')
                LimitCounter += 1
                while(LimitCounter > self.Limit):
                    if Date() - LimitTimer > 60:
                        LimitCounter = 1
                        LimitTimer = Date()
                    Chronus.Sleep(1)

            if self.Mode == 'Thread':
                while(CONTINUE):
                    for Item in range(ParallelNumber):
                        if (WorkSpace[Item] == None) or (WorkSpace[Item].isAlive() == False):
                            CONTINUE = False
                            AvailableThread = Item
                            break
                        
                WorkSpace[AvailableThread] = threading.Thread(target = Task[0], args = Task[1])
                WorkSpace[AvailableThread].start() 

            elif self.Mode == 'Process':
                while(CONTINUE):
                    for Item in range(ParallelNumber):
                        if (WorkSpace[Item] == None) or (WorkSpace[Item].is_alive() == False):
                            CONTINUE = False
                            AvailableThread = Item
                            break
                    Chronus.Sleep(1)
                        
                WorkSpace[AvailableThread] = threading.Thread(target = Task[0], args = Task[1])
                WorkSpace[AvailableThread].start() 

        for Item in WorkSpace:
            if Item != None:
                Item.join() 

        if self.Timer:   
            TimeConsumed = round(float(time.time() - StartTime), 3)
            print('\n\t***Time-Consuming: ***\n\t' + str(TimeConsumed) + 's')


    def GetList(self):
        return multiprocessing.Manager().list() 

class ThreadMatix:
    def __init__(self, Core, Thread, Limit = None):
        self.Core = Core
        self.Thread = Thread
        self.TaskList = []
        self.Limit = Limit

        for Item in range(self.Core):
            self.TaskList.append([])
        self.AutoArrangedTaskList = []


    def NewTask(self, Core, Function, Arguments):
        self.TaskList[Core-1].append([Function, tuple(Arguments)])

    def NewTasks(self, Core, Group, Function, Arguments):
        for Item in Group:
            self.TaskList[Core-1].append([Function, tuple([Item]+Arguments)])


    def NewTaskAutoArrange(self, Function, Arguments):
        self.AutoArrangedTaskList.append([Function, tuple(Arguments)])

    def NewTasksAutoArrange(self, Group, Function, Arguments):
        for Item in Group:
            self.AutoArrangedTaskList.append([Function, tuple([Item]+Arguments)])


    def NewProcess(self, Core):
        TP = ThreadPool('Thread', Limit = self.Limit)
        TP.TaskList = self.TaskList[Core]
        TP.Start(self.Thread)


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

        TP = ThreadPool('Process')
        TP.NewTasks(range(self.Core), self.NewProcess, [])

        TP.Start(self.Core)

    
    def GetList(self):
        return multiprocessing.Manager().list() 


def MultCoreTasks(Core, Thread, Group, Args, Limit=False):
    def RetFunc(Fn):
        TM = ThreadMatix(Core, Thread, Limit=Limit)
        TM.NewTasksAutoArrange(Group, Fn, Args)
        TM.Start()
    return RetFunc

def MultThreadTasks(Thread, Group, Args, Limit=False):
    def RetFunc(Fn):
        TM = ThreadPool('Thread', Limit=Limit)
        TM.NewTasks(Group, Fn, Args)
        TM.Start(Thread)
    return RetFunc