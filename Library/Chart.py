from pyecharts import *
from pyecharts.charts import *

#[[x], {A:[B]}]
def GetBar(Data):
    Ret = (
        Bar()
        .add_xaxis(Data[0])
    )
    for Item in Data[1]:
        Ret.add_yaxis(Item, Data[1][Item])
    return Ret

def GetLine(Data):
    Ret = (
        Line()
        .add_xaxis(Data[0])
    )
    for Item in Data[1]:
        Ret.add_yaxis(Item, Data[1][Item])
    return Ret

def GetKLine(Data):
    Ret = (
        KLine()
        .add_xaxis(Data[0])
    )
    for Item in Data[1]:
        Ret.add_yaxis(Item, Data[1][Item])
    return Ret

def GetScatter(Data):
    Ret = (
        Scatter()
        .add_xaxis(Data[0])
    )
    for Item in Data[1]:
        Ret.add_yaxis(Item, Data[1][Item])
    return Ret

def MergeChart(Main, Sub):
    for Item in Sub:
        Main.overlap(Item)

def GridVertical(ChartF, ChartS, SplitP):
    ArgL = str(SplitP) + '%'
    ArgR = str(100-SplitP) + '%'
    return (
        Grid()
        .add(ChartS, grid_opts=options.GridOpts(pos_left=ArgL))
        .add(ChartF, grid_opts=options.GridOpts(pos_right=ArgR))
    )

def GridHorizontal(ChartF, ChartS, SplitP):
    ArgT = str(SplitP) + '%'
    ArgB = str(100-SplitP) + '%'
    return (
        Grid()
        .add(ChartS, grid_opts=options.GridOpts(pos_top=ArgT))
        .add(ChartF, grid_opts=options.GridOpts(pos_bottom=ArgB))
    )
    
def RenderChart(Plot, OutputLocation):
    Plot.render(OutputLocation)