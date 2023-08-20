import sys
import os
import platform
import ac
import acsys 

if platform.architecture()[0] == "64bit":
    dllfolder = "third_party\stdlib64"
else:
    dllfolder = "third_party\stdlib"
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(cwd, dllfolder))

from sim_info import info

l_steering = 0
gforce = 0
steer = 0
l_currentminspeed = 0
currentminspeed = -1
lastminspeed = 0
oldspeed = 0
l_sector = 0
currentsector = 1
oldsector = 0
l_sector1avg = 0
l_sector2avg = 0
l_sector3avg = 0

sector1avg = 0
sector2avg = 0
sector3avg = 0

sector1speeds = list()
sector2speeds = list()
sector3speeds = list()

l_laps = 0
laps = 0
oldlaps = 0

def Average(lst):
    return int(sum(lst) / len(lst))

def acMain(ac_version):
    global l_currentminspeed,l_steering,l_sector,l_sector1avg,l_sector2avg,l_sector3avg,sector1avg,sector2avg,sector3avg,l_laps

    appWindow = ac.newApp("minimum speed indicator")
    ac.setSize(appWindow, 400, 400)

    ac.console("ACMinSpeed Loaded!")

    l_currentminspeed = ac.addLabel(appWindow, "minspeed: 0")
    l_sector = ac.addLabel(appWindow, "test var: ")
    l_laps = ac.addLabel(appWindow, "completed laps: 0")
    l_sector1avg = ac.addLabel(appWindow, "sector 1: 0")
    l_sector2avg = ac.addLabel(appWindow, "sector 2: 0")
    l_sector3avg = ac.addLabel(appWindow, "sector 3: 0")

    ac.setPosition(l_currentminspeed, 3, 30)
    ac.setPosition(l_sector, 3, 60)
    ac.setPosition(l_laps, 3, 90)
    ac.setPosition(l_sector1avg, 3, 120)
    ac.setPosition(l_sector2avg, 3, 150)
    ac.setPosition(l_sector3avg, 3, 180)

    return "minimum speed indicator"
    

def acUpdate(deltaT):
    
    global l_currentminspeed,oldspeed,l_steering,currentminspeed,lastminspeed,l_sector,currentsector,oldsector,l_sector1avg,l_sector2avg,l_sector3avg,sector1speeds,sector2speeds,sector3speeds,l_laps,laps,oldlaps

    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    steer = ac.getCarState(0, acsys.CS.Steer)
    laps = info.graphics.completedLaps
    ac.setText(l_laps, "completed laps: {}".format(laps))

    abs_steer = abs(steer)
    speed = int(speed)
    currentsector = info.graphics.currentSectorIndex + 1
    labelstring = "current sector: " + str(currentsector)
    ac.setText(l_sector, labelstring)

    if speed < oldspeed and abs_steer > 15:
        if currentminspeed == -1:
            currentminspeed = speed

        if speed < currentminspeed:
            currentminspeed = speed

        lastminspeed = currentminspeed
        ac.setText(l_currentminspeed, "minspeed: {}".format(lastminspeed))

    if speed > lastminspeed and abs_steer < 15:
        ac.setText(l_currentminspeed, "minspeed: {}".format(lastminspeed))
        currentminspeed = -1
        
    oldspeed = speed

    if currentsector  == 1:
        sector1speeds.append(speed)
    if currentsector  == 2:
        sector2speeds.append(speed)
    if currentsector  == 3:
        sector3speeds.append(speed)
    
    if currentsector != oldsector:
        if currentsector == 2:
            sector1avg = Average(sector1speeds)
            ac.setText(l_sector1avg, "sector 1: {}".format(sector1avg))
            sector1speeds.clear
        if currentsector == 3:
            sector2avg = Average(sector2speeds)
            ac.setText(l_sector2avg, "sector 2: {}".format(sector2avg))
            sector2speeds.clear
        if currentsector == 1:
            sector3avg = Average(sector3speeds)
            ac.setText(l_sector3avg, "sector 3: {}".format(sector3avg))
            sector3speeds.clear
    if laps != oldlaps:
        sector1speeds.clear()
        sector2speeds.clear()
        sector3speeds.clear()



    oldlaps = laps
    oldsector = currentsector

def acShutdown():
   # ...
   return