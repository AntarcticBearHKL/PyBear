import calendar
import datetime
import time

import PyBear.Bear as Bear

class Date:
    def __init__(self, Load=None, TimeShift=None):
        if type(Load) == Date:
            self.Time = Load.Time
            self.TimeShift = Load.TimeShift
        elif type(Load) == datetime.datetime:
            self.Time = Load
            if type(TimeShift) == int:
                self.TimeShift = TimeShift 
            else:
                self.TimeShift = Bear.LocalTimeZoneShift  
        elif len(str(Load)) == 17:
            Load = str(Load)
            self.Time = datetime.datetime(
                int(Load[0:4]), int(Load[4:6]), int(Load[6:8]), 
                int(Load[8:10]), int(Load[10:12]), int(Load[12:14]))
            self.TimeShift = int(Load[15:16])
        elif len(str(Load)) == 8:
            Load = str(Load)
            self.Time = datetime.datetime(
                int(Load[0:4]), int(Load[4:6]), int(Load[6:8]), 
                0, 0, 0)
            if type(TimeShift) == int:
                self.TimeShift = TimeShift 
            else:
                self.TimeShift = Bear.LocalTimeZoneShift 
        elif len(str(Load)) == 14:
            Load = str(Load)
            self.Time = datetime.datetime(
                int(Load[0:4]), int(Load[4:6]), int(Load[6:8]), 
                int(Load[8:10]), int(Load[10:12]), int(Load[12:14]))
            if type(TimeShift) == int:
                self.TimeShift = TimeShift 
            else:
                self.TimeShift = Bear.LocalTimeZoneShift 
        elif len(str(Load)) == 24:
            Load = str(Load)
            self.Time = datetime.datetime.fromisoformat(Load[:-5])
            self.TimeShift = 0
        else:
            self.Time = datetime.datetime.now()
            self.TimeShift = Bear.LocalTimeZoneShift
        self.TimeZoneRectification(Shift=Bear.LocalTimeZoneShift)

    def String(self, Style=999, Raw=False):
        if Style == 1:
            Style = '%Y-%m-%d'
        elif Style == 2:
            Style = '%Y-%m-%d %H:%M:%S'
        elif Style == -1:
            Style = '%Y%m%d'
        elif Style == -2:
            Style = '%Y%m%d%H%M%S'
        else:
            Style = '%Y-%m-%d %H:%M:%S'
        
        if Raw:
           return self.Time.strftime(Style)
        return self.Time.strftime(Style) + '(' + str(self.TimeShift) + ')'

    def ISOString(self):
        return Date(self).TimeZoneRectification().Time.isoformat().split('.')[0]+'.000Z'

    def SetTime(self, Year=None, Month=None, Day=None, Hour=None, Minute=None, Second=None):
        if Year:
            NYear = Year
        else:
            NYear = self.YearInt()

        if Month:
            NMonth = Month
        else:
            NMonth = self.MonthInt()
        
        if Day:
            if Day == 999:
                NDay = CalEnder(Year=NYear, Month=NMonth).HowManyDays()
            else:
                NDay = Day
        else:
            NDay = self.DayInt()
        
        if Hour:
            NHour = Hour
        else:
            NHour = self.HourInt()

        if Minute:
            NMinute = Minute
        else:
            NMinute = self.MinuteInt()

        if Second:
            NSecond = Second
        else:
            NSecond = self.SecondInt()

        self.Time = datetime.datetime(NYear, NMonth, NDay, NHour, NMinute, NSecond)
        return self
            
    def Shift(self, Year=0, Month=0, Day=0, Hour=0, Minute=0, Second=0):
        NYear = self.YearInt() + Year

        NMonth = self.MonthInt() + Month
        NYear += (NMonth - 1) // 12
        NMonth = ((NMonth - 1) % 12) + 1

        Base = datetime.datetime(
            NYear, NMonth, self.DayInt(), 
            self.HourInt(), self.MinuteInt(), self.SecondInt())

        TimePlus = datetime.timedelta(days=Day, hours=Hour, minutes=Minute, seconds=Second) 
    
        self.Time = Base + TimePlus
        return self

    def TimeZoneRectification(self, Shift=None):
        if not Shift:
            Shift = 0
        TimeShiftDelta = Shift - self.TimeShift
        self.Shift(Hour=TimeShiftDelta)
        self.TimeShift = Shift
        return self


    def Year(self):
        return str(self.Time.date().year)

    def Month(self):
        Ret = self.Time.date().month
        if Ret < 10:
            return '0' + str(Ret)
        else:
            return str(Ret)

    def Day(self):
        return str(self.Time.date().day)

    def Hour(self):
        return str(self.Time.time().hour)

    def Minute(self):
        return str(self.Time.time().minute)

    def Second(self):
        return str(self.Time.time().second)


    def YearInt(self):
        return int(self.Time.date().year)

    def MonthInt(self):
        return int(self.Time.date().month)

    def DayInt(self):
        return int(self.Time.date().day)

    def HourInt(self):
        return int(self.Time.time().hour)

    def MinuteInt(self):
        return int(self.Time.time().minute)

    def SecondInt(self):
        return int(self.Time.time().second)


    def __floordiv__(self, Rhs): #[Y,M,D,h,m,s] (//)
        Ret = []
        Ret.append(self.YearInt()- Rhs.YearInt())
        Ret.append(self.MonthInt()- Rhs.MonthInt())
        Ret.append(self.DayInt()- Rhs.DayInt())
        Ret.append(self.HourInt()- Rhs.HourInt())
        Ret.append(self.MinuteInt()- Rhs.MinuteInt())
        Ret.append(self.SecondInt()- Rhs.SecondInt())
        return Ret

    def __sub__(self, Rhs): # How Much Second (-)
        Ret = 0
        TimeList = self // Rhs
        YearStart = Rhs.YearInt()
        MonthStart = Rhs.MonthInt()
        MonthDays = calendar.mdays
        for Item in range(TimeList[0]):
            YearDays = 366 if calendar.isleap(int(str(YearStart))) else 365
            Ret += YearDays * 86400
            YearStart += 1
        for Item in range(abs(TimeList[1])):
            if TimeList[1]>0:
                Ret+= MonthDays[MonthStart] * 86400
                MonthStart += 1
            else:
                Ret-= MonthDays[Item+ 1] * 86400
        Ret += TimeList[2]*86400 + TimeList[3]*3600 + TimeList[4]*60 + TimeList[5]
        return Ret


    def __lt__(self, Rhs):
        if self.Time.ShiftRectification() < Rhs.Time.ShiftRectification():
            return True
        else:
            return False
 
    def __le__(self, Rhs):
        if self.Time.ShiftRectification() <= Rhs.Time.ShiftRectification():
            return True
        else:
            return False

    def __gt__(self, Rhs):
        if self.Time.ShiftRectification() > Rhs.Time.ShiftRectification():
            return True
        else:
            return False

    def __ge__(self, Rhs):
        if self.Time.ShiftRectification() >= Rhs.Time.ShiftRectification():
            return True
        else:
            return False

    def __eq__(self, Rhs):
        if self.Time.ShiftRectification() == Rhs.Time.ShiftRectification():
            return True
        else:
            return False

    def __ne__(self, Rhs):
        if self.Time.ShiftRectification() != Rhs.Time.ShiftRectification():
            return True
        else:
            return False


class Calender:
    def __init__(self, Year = None, Month = None, Day = None):
        if Year:
            self.Year = int(Year)
        else:
            self.Year = Date().YearInt()

        if Month:
            self.Month = int(Month)
        else:
            self.Month = Date().MonthInt()

        if Day:
            self.Day = int(Day)
        else:
            self.Day = Date().DayInt()


    def Year(self):
        return self.Year

    def Month(self):
        return self.Month

    def Day(self):
        return self.Day


    def DaysOfMonth(self):
        return calendar.monthrange(int(self.Year), int(self.Month))[1]

    def DaysOfYear(self):
        Month = 1
        Ret = 0
        while Month<13:
            Ret += calendar.monthrange(int(self.Year), int(Month))[1]
            Month += 1
        return Ret


    def DaysRemainingOfMonth(self):
        return self.DaysOfMonth() - Date().DayInt()
    
    def DaysRemainingOfYear(self):
        Month = self.Month + 1
        Ret = 0
        while Month<13:
            Ret += calendar.monthrange(int(self.Year), int(Month))[1]
            Month += 1
        Ret += self.DaysRemainingOfMonth()
        return Ret


Timer = {}
def Timer(Name):
    if Name not in Timer:
        Timer[Name] = datetime.datetime.now()
    else:
        print(datetime.datetime.now() - Timer[Name])

def Clock():
    return Date().String()

def SecToTime(sec):
    return '''%ss = %s year %s month %s day %s hour %s minute %s second'''%(
        str(sec), 
        str((sec % 1) // 31557600),
        str((sec % 31557600) // 2629800),
        str((sec % 2629800) // 86400),
        str((sec % 86400) // 3600),
        str((sec % 3600) // 60),
        str((sec % 60) // 1),
        )

def MonthToStr(Month):
    Month = int(Month)
    if Month < 10:
        return '0' + str(Month)
    else:
        return str(Month)

def Sleep(Sec):
    time.sleep(Sec)

def Alarm(Day = 0, Hour = 0, Minute = 0, Second = 0):
    print ('\t----------START AT: ' + Clock() + '----------')
    if Day != 0 or Hour != 0 or Minute != 0 or Second != 0:
        Interval = Day*60*60*24 + Hour*60*60 + Minute*60 + Second
        time.sleep(Interval)
    else:
        return -1
    print ('\t---------- END  AT: ' + Clock() + '----------')

def HeartBeatTask(Fn, Hour=0, Minute=0, Second=0):
    if not Hour and not Minute and not Second:
        print('Parameter Error')
        exit()
    WaitSecond = Hour*3600 + Minute*60 + Second
    while(True):
        print('\nSchedule Start At : ' + Clock() + ' : Call Function: "' + Fn.__name__ + '" & Return :')
        Fn()
        print('Schedule End At : ' + Clock())
        Sleep(WaitSecond)

def ScheduleTask(Fn, Timer):
    class Schedule:
        def __init__(self, Timer):
            self.Timer = Timer.split(':')
            if len(self.Timer) == 1:
                Step = Date().String(-2)
                Step = Step[0:12] + ''.join(self.Timer)
                self.lastStep = Date(Step)
                self.nextRound = self.MinuteSche
            elif len(self.Timer) == 2:
                Step = Date().String(-2)
                Step = Step[0:10] + ''.join(self.Timer)
                self.lastStep = Date(Step)
                self.nextRound = self.hourSche
            elif len(self.Timer) == 3:
                Step = Date().String(-2)
                Step = Step[0:8] + ''.join(self.Timer)
                self.lastStep = Date(Step)
                self.nextRound = self.daySche
            else:
                print('parameter error')
                exit()
        
        def MinuteSche(self):
            if Date()-self.lastStep >= 60:
                Step = Date().String(-2)
                Step = Step[0:12] + ''.join(self.Timer)
                self.lastStep = Date(Step)
                return True
            return False

        def HourSche(self):
            if Date()-self.lastStep >= 3600:
                Step = Date().String(-2)
                Step = Step[0:10] + ''.join(self.Timer)
                self.lastStep = Date(Step)
                return True
            return False

        def DaySche(self):
            if Date()-self.lastStep >= 86400:
                Step = Date().String(-2)
                Step = Step[0:8] + ''.join(self.Timer)
                self.lastStep = Date(Step)
                return True  
            return False         

    Schedule = Schedule(Timer)
    while(True):
        if Schedule.nextRound():
            print('\nSchedule Start At : ' + Clock() + ' : Call Function: "' + Fn.__name__ + '" & Return :')
            Fn()
            print('Schedule End At : ' + Clock())
        Sleep(1)

def GetInterval_Day(Start, End):
    Starty = Date(Start).YearInt()
    Startm = Date(Start).MonthInt()
    Startd = Date(Start).DayInt()
    Endy = Date(End).year()
    Endm = Date(End).month()
    Endd = Date(End).DayInt()
    ret = []
    for month in CalEnder.getBetweenMonth(Start, End):
        MonthDays = CalEnder.getDayNum(int(month[0:4]), int(month[4:6]))
        while True:
            if Startd<10:
                ret.append(str(month) + '0' + str(Startd))
            else:
                ret.append(str(month)+str(Startd))
            Startd += 1
            if (str(month) == (Endy + Endm)) and Startd > Endd:
                break
            if Startd > MonthDays:
                Startd = 1
                break
    return ret

def GetInterval_Month(Start, End):
    Starty = Date(Start).YearInt()
    Startm = Date(Start).MonthInt()
    Endy = Date(End).YearInt()
    Endm = Date(End).MonthInt()
    ret = []
    for year in CalEnder.getBetweenYear(Start, End):
        while True:
            if Startm<10:
                ret.append(str(year) + '0' + str(Startm))
            else:
                ret.append(str(year)+str(Startm))
            Startm += 1
            if Startm > 12:
                Startm = 1
                break
            if year == Endy and Startm > Endm:
                break
    return ret

def GetInterval_Year(Start, End):
    Starty = Date(Start).YearInt()
    Endy = Date(End).YearInt()
    ret = []
    while True:
        ret.append(Starty)
        Starty += 1
        if Starty > Endy:
            break
    return ret

def DateClip(Line, Start, End):
    _Start = None
    _End = None
    for _count in range(len(Line) - 1):
        if Date(Line[_count]) < Date(Start) <= Date(Line[_count + 1]):
            _Start = _count + 1
        if Date(Line[_count]) <= Date(End) < Date(Line[_count + 1]):
            _End = _count
        if Date(Start) == Date(Line[_count]):
            _Start = _count
        if Date(End) == Date(Line[_count + 1]):
            _End = _count + 1
    return [_Start, _End]

if Bear.TestUnit:
    pass