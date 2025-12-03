import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from math import exp

xExp = 1
rExp = 1.1

xLog = 0.01
rLog = 2

xMor = .01
rMor = 2

xPar = 0.04
yPar = 0.01
a = 1
b = 1
c = 1


xExpVals = []
xLogVals = []
xMorVals = []
xParVals = []
yParVals = []

tEnd = 36


def expGrow(x, r):
    return r*x


def logicGrow(x, r):
    return min(r*x*(1-x),1)


def moranGrow(x, r):
    return x*exp(r*(1-x))


def parasite(x, y, a, b, c):
    x_ = b*x*exp(-a*y)
    y_ = c*x*(1-exp(-a*y))
    return x_, y_


def updateExpVals(r):
    xExpVals.clear()

    x = xExp

    xExpVals.append(x)
    for i in range(tEnd):
        x = expGrow(x, r)
        xExpVals.append(x)


def updateLogVals(r):
    xLogVals.clear()

    x = xLog

    xLogVals.append(x)
    for i in range(tEnd):
        x = logicGrow(x, r)
        xLogVals.append(x)


def updateMorVals(r):
    xMorVals.clear()

    x = xMor

    xMorVals.append(x)
    for i in range(tEnd):
        x = moranGrow(x, r)
        xMorVals.append(x)


def updateParVals(a,b,c):
    xParVals.clear()
    yParVals.clear()
    x = xPar
    y = yPar

    xParVals.append(x)
    yParVals.append(y)
    for i in range(tEnd):
        x, y = parasite(x, y, a, b, c)
        xParVals.append(x)
        yParVals.append(y)


# Define initial parameters
updateExpVals(rExp)
updateLogVals(rLog)
updateMorVals(rMor)
updateParVals(a,b,c)


figExp, axExp = plt.subplots()
axExp.set_title("Exponential grow")
lineExp, = axExp.plot(xExpVals)
plt.grid()

figExp.subplots_adjust(left=0.25, bottom=0.25)
axExpEx = figExp.add_axes([0.25, 0.1, 0.65, 0.03])

rExpSlider = Slider(
    ax=axExpEx,
    label='r Exp',
    valmin=0,
    valmax=7,
    valinit=rExp,
)


def expSliderUpdate(val):
    updateExpVals(rExpSlider.val)
    lineExp.set_ydata(xExpVals)
    axExp.set_xlim([0, tEnd])
    axExp.set_ylim([0, max(xExpVals)])


rExpSlider.on_changed(expSliderUpdate)
expSliderUpdate(rExp)


figLog, axLog = plt.subplots()
axLog.set_title("Logical model")
lineLog, = axLog.plot(xLogVals)
plt.grid()

figLog.subplots_adjust(left=0.25, bottom=0.25)
axLogEx = figLog.add_axes([0.25, 0.1, 0.65, 0.03])

rLogSlider = Slider(
    ax=axLogEx,
    label='r Log',
    valmin=0,
    valmax=7,
    valinit=rLog,
)


def logSliderUpdate(val):
    updateLogVals(val)
    lineLog.set_ydata(xLogVals)
    axLog.set_xlim([0, tEnd])
    axLog.set_ylim([0, 1])


rLogSlider.on_changed(logSliderUpdate)
logSliderUpdate(rLog)


figMor, axMor = plt.subplots()
axMor.set_title("Moran's model")
lineMor, = axMor.plot(xMorVals)
plt.grid()

figMor.subplots_adjust(left=0.25, bottom=0.25)
axMorEx = figMor.add_axes([0.25, 0.1, 0.65, 0.03])

rMorSlider = Slider(
    ax=axMorEx,
    label='r Mor',
    valmin=0,
    valmax=5,
    valinit=rMor,
)


def morSliderUpdate(val):
    updateMorVals(rMorSlider.val)
    lineMor.set_ydata(xMorVals)
    axMor.set_xlim([0, tEnd])
    axMor.set_ylim([0, 10])


rMorSlider.on_changed(morSliderUpdate)
morSliderUpdate(rMor)


figPar, axPar = plt.subplots()
axPar.set_title("Parasitics model")
lineParx, = axPar.plot(xParVals)
linePary, = axPar.plot(yParVals)
plt.grid()

figPar.subplots_adjust(left=0.3, bottom=0.4)
axParEx = figPar.add_axes([0.25, 0.3, 0.65, 0.03])
bxParEx = figPar.add_axes([0.25, 0.2, 0.65, 0.03])
cxParEx = figPar.add_axes([0.25, 0.1, 0.65, 0.03])

aParSlider = Slider(
    ax=axParEx,
    label='a',
    valmin=0,
    valmax=7,
    valinit=a,
)
bParSlider = Slider(
    ax=bxParEx,
    label='b',
    valmin=0,
    valmax=7,
    valinit=b,
)
cParSlider = Slider(
    ax=cxParEx,
    label='c',
    valmin=0,
    valmax=7,
    valinit=c,
)


def parSliderUpdate(val):
    updateParVals(aParSlider.val,bParSlider.val,cParSlider.val)
    lineParx.set_ydata(xParVals)
    linePary.set_ydata(yParVals)
    axPar.set_xlim([0, tEnd])
    axPar.set_ylim([0, max(max(xParVals),max(yParVals))])


aParSlider.on_changed(parSliderUpdate)
bParSlider.on_changed(parSliderUpdate)
cParSlider.on_changed(parSliderUpdate)
parSliderUpdate(rMor)


plt.show()
