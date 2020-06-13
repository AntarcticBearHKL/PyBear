import calendar
import datetime
import time
import sys,os
from dateutil import tz
from dateutil.tz import tzlocal

import PyBear.GlobalBear as GlobalBear

class Date:
    def __init__(self, Load=None, TimeShift=None):
        if type(Load) == datetime.datetime and TimeShift:
            self.Time = Load
            self.TimeShift = TimeShift      
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
            if not TimeShift:
                self.TimeShift = GlobalBear.LocalTimeZoneShift
            else:
                self.TimeShift = TimeShift
        else:
            self.Time = datetime.datetime.now()
            self.TimeShift = GlobalBear.LocalTimeZoneShift

    def String(self, Style):
        if Style == 1:
            Style = '%Y-%m-%d'
        elif Style == 2:
            Style = '%Y-%m-%d %H:%M:%S'
        elif Style == -1:
            Style = '%Y%m%d'
            return self.Time.strftime(Style)
        else:
            Style = '%Y%m%d%H%M%S'
        return self.Time.strftime(Style) + '(' + str(self.TimeShift) + ')'

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
                NDay = Calender(Year=NYear, Month=NMonth).HowManyDays()
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
        NYear += NMonth // 12
        NMonth = NMonth % 12

        Base = datetime.datetime(
            NYear, NMonth, self.DayInt(), 
            self.HourInt(), self.MinuteInt(), self.SecondInt(), tzinfo=TimeZoneZero)

        TimePlus = datetime.timedelta(days=Day, hours=Hour, minutes=Minute, seconds=Second) 
    
        self.Time = Base + TimePlus
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
        if self.Time < Rhs.Time:
            return True
        else:
            return False
 
    def __le__(self, Rhs):
        if self.Time <= Rhs.Time:
            return True
        else:
            return False

    def __gt__(self, Rhs):
        if self.Time > Rhs.Time:
            return True
        else:
            return False

    def __ge__(self, Rhs):
        if self.Time >= Rhs.Time:
            return True
        else:
            return False

    def __eq__(self, Rhs):
        if self.Time == Rhs.Time:
            return True
        else:
            return False

    def __ne__(self, Rhs):
        if self.Time != Rhs.Time:
            return True
        else:
            return False


class Calender:
    def __init__(self, Year = None, Month = None):
        if Year:
            self.Year = str(Year)
        else:
            self.Year = Date().Year()

        if Month:
            self.Month = self.GetMonth(Month)
        else:
            self.Month = self.GetMonth(None)

    def GetMonth(self, Month):
        if not Month:
            return Date().Month()
        else:
            if Month < 10:
                return '0' + str(Month)
            else:
                return str(Month)

    def HowManyDays(self):
        return calendar.monthrange(int(self.Year), int(self.Month))[1]
 
    def DayRange(self):
        Days = self.HowManyDays()
        return [Date().ResetTime(Day=1).String(Style=Style_SS), Date().ResetTime(Day=Days).String(Style=Style_SS)]


Timer = {}
class Chronus:
    def Timer(Name):
        if Name not in Timer:
            Timer[Name] = datetime.datetime.now()
        else:
            print(datetime.datetime.now() - Timer[Name])

    def Clock():
        return Date().to_string()

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

    def Sleep(sec):
        time.sleep(sec)

    def Alarm(day = 0, hour = 0, minute = 0, second = 0):
        print ('\t----------START AT: ' + Chronus.Clock() + '----------')
        if day != 0 or hour != 0 or minute != 0 or second != 0:
            _interval = day*60*60*24 + hour*60*60 + minute*60 + second
            time.sleep(_interval)
        else:
            return -1
        print ('\t---------- END  AT: ' + Chronus.Clock() + '----------')

    def IntervalSchedule(fn, hour=0, minute=0, second=0):
        if hour==0 and minute==0 and second==0:
            print('parameter error')
            exit()
        waitSecond = hour*3600 + minute*60 + second
        while(True):
            print('\nSchedule start at : ' + Chronus.Clock() + ' : call function: ' + fn.__name__ + ' : and return :')
            fn()
            print('Schedule end at : ' + Chronus.Clock())
            Sleep(waitSecond)

    def TimedSchedule(fn, timer):
        class Schedule:
            def __init__(self, timer):
                self.Timer = timer.split(':')
                if len(self.Timer) == 1:
                    step = Date().to_string()
                    step = step[0:12] + ''.join(self.Timer)
                    self.lastStep = Date(step)
                    self.nextRound = self.MinuteSche
                elif len(self.Timer) == 2:
                    step = Date().to_string()
                    step = step[0:10] + ''.join(self.Timer)
                    self.lastStep = Date(step)
                    self.nextRound = self.hourSche
                elif len(self.Timer) == 3:
                    step = Date().to_string()
                    step = step[0:8] + ''.join(self.Timer)
                    self.lastStep = Date(step)
                    self.nextRound = self.daySche
                else:
                    print('parameter error')
                    exit()
            
            def MinuteSche(self):
                if Date()-self.lastStep >= 60:
                    step = Date().to_string()
                    step = step[0:12] + ''.join(self.Timer)
                    self.lastStep = Date(step)
                    return True
                return False

            def HourSche(self):
                if Date()-self.lastStep >= 3600:
                    step = Date().to_string()
                    step = step[0:10] + ''.join(self.Timer)
                    self.lastStep = Date(step)
                    return True
                return False

            def DaySche(self):
                if Date()-self.lastStep >= 86400:
                    step = Date().to_string()
                    step = step[0:8] + ''.join(self.Timer)
                    self.lastStep = Date(step)
                    return True  
                return False         

        Schedule = Schedule(timer)
        while(True):
            if Schedule.nextRound():
                print('\nSchedule start at : ' + Date().to_string(style='L1') + ' : call function: "' + fn.__name__ + '" and return :')
                fn()
                print('Schedule end at : ' + Date().to_string(style='L1'))
            Chronus.Sleep(1)

    def GetBetweenDay(start, end):
        starty = Date(start).YearInt()
        startm = Date(start).MonthInt()
        startd = Date(start).DayInt()
        endy = Date(end).year()
        endm = Date(end).month()
        endd = Date(end).DayInt()
        ret = []
        for month in Calender.getBetweenMonth(start, end):
            MonthDays = Calender.getDayNum(int(month[0:4]), int(month[4:6]))
            while True:
                if startd<10:
                    ret.append(str(month) + '0' + str(startd))
                else:
                    ret.append(str(month)+str(startd))
                startd += 1
                if (str(month) == (endy + endm)) and startd > endd:
                    break
                if startd > MonthDays:
                    startd = 1
                    break
        return ret

    def GetBetweenMonth(start, end):
        starty = Date(start).YearInt()
        startm = Date(start).MonthInt()
        endy = Date(end).YearInt()
        endm = Date(end).MonthInt()
        ret = []
        for year in Calender.getBetweenYear(start, end):
            while True:
                if startm<10:
                    ret.append(str(year) + '0' + str(startm))
                else:
                    ret.append(str(year)+str(startm))
                startm += 1
                if startm > 12:
                    startm = 1
                    break
                if year == endy and startm > endm:
                    break
        return ret

    def GetBetweenYear(start, end):
        starty = Date(start).YearInt()
        endy = Date(end).YearInt()
        ret = []
        while True:
            ret.append(starty)
            starty += 1
            if starty > endy:
                break
        return ret

    def DateClip(line, start, end):
        _start = None
        _end = None
        for _count in range(len(line) - 1):
            if Date(line[_count]) < Date(start) <= Date(line[_count + 1]):
                _start = _count + 1
            if Date(line[_count]) <= Date(end) < Date(line[_count + 1]):
                _end = _count
            if Date(start) == Date(line[_count]):
                _start = _count
            if Date(end) == Date(line[_count + 1]):
                _end = _count + 1
        return [_start, _end]

if GlobalBear.GlobalTestModuleOn:
    pass