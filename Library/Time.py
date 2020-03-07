import calendar
import datetime
import time
import sys,os

from PyBear.GlobalBear import *

Style_SS = '%Y%m%d'
Style_SL = '%Y%m%d%H%M%S'
Style_M = '%Y-%m-%d'
Style_L = '%Y-%m-%d %H:%M:%S'
Style_Raw = '%Y %m %d %H %M %S'

class Date:
    def __init__(self, Load=False):
        if Load:
            if type(Load) == datetime.datetime:
                self.Time = str(Load)
            elif len(str(Load).split('.')) == 2:
                self.Time = datetime.datetime.fromtimestamp(Load)
            elif len(str(Load).split('-')) == 3:
                Load = str(Load) + ' 00:00:00'
                self.Time = datetime.datetime.strptime(Load, '%Y-%m-%d %H:%M:%S')
            elif len(str(Load)) == 14:
                Load = str(Load)
                Load = Load[0:4] + '-' + Load[4:6] + '-' + Load[6:8] + '  ' + Load[8:10] + ':' + Load[10:12] + ':' + Load[12:14]
                self.Time = datetime.datetime.strptime(Load, '%Y-%m-%d %H:%M:%S')
            elif len(str(Load).split('-')) == 1:
                Load = str(Load)
                Load = Load[0:4] + '-' + Load[4:6] + '-' + Load[6:8] + ' 00:00:00'
                self.Time = datetime.datetime.strptime(Load, '%Y-%m-%d %H:%M:%S')
        else:
            self.Time = datetime.datetime.now()


    def String(self, Style = Style_SL):
        return self.Time.strftime(Style)

    def Timestamp(self):
        return time.mktime(self.Time.timetuple()), int(time.mktime(self.Time.timetuple()))

        return int(time.mktime(self.Time.timetuple()))


    def Year(self):
        return str(self.Time.date().year)

    def Month(self):
        ret = self.Time.date().month
        if ret < 10:
            return '0' + str(ret)
        else:
            return str(ret)

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


    def __floordiv__(self, Rhs):
        Ret = []
        Ret.append(self.YearInt()- Rhs.YearInt())
        Ret.append(self.MonthInt()- Rhs.MonthInt())
        Ret.append(self.DayInt()- Rhs.DayInt())
        Ret.append(self.HourInt()- Rhs.HourInt())
        Ret.append(self.MinuteInt()- Rhs.MinuteInt())
        Ret.append(self.SecondInt()- Rhs.SecondInt())
        return Ret

    def __sub__(self, Rhs):
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
    def __init__(self):
        self.getDays = calendar.monthrange

    def GetDay(self):
        return DS(datetime.datetime.now())

    def GetMonth(self):
        mmonth = int(month(datetime.datetime.now()))
        if mmonth<10:
            mmonth = '0' + str(mmonth)
        else:
            mmonth = str(mmonth)
        return year(datetime.datetime.now()) + '-' + mmonth

    def GetYear(self):
        return year(datetime.datetime.now())

    def GetDayNum(self, year, month):
        return calendar.monthrange(year, month)[1]


class Chronus:
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
        print ('\t----------START AT: ' + str(now()) + '----------')
        if day != 0 or hour != 0 or minute != 0 or second != 0:
            _interval = day*60*60*24 + hour*60*60 + minute*60 + second
            time.sleep(_interval)
        else:
            return -1
        print ('\t---------- END  AT: ' + str(now()) + '----------')

    def IntervalSchedule(fn, hour=0, minute=0, second=0):
        if hour==0 and minute==0 and second==0:
            print('parameter error')
            exit()
        waitSecond = hour*3600 + minute*60 + second
        while(True):
            print('\nSchedule start at : ' + Chronus.clock() + ' : call function: ' + fn.__name__ + ' : and return :')
            fn()
            print('Schedule end at : ' + Chronus.clock())
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

if GlobalAvailabilityCheck:
    pass