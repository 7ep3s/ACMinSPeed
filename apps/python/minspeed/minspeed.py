import sys
import os
import platform
if platform.architecture()[0] == "64bit":
    dllfolder = "third_party\stdlib64"
else:
    dllfolder = "third_party\stdlib"
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(cwd, dllfolder))
import ac
import acsys 





from sim_info import info

l_steering = 0
gforce = 0
steer = 0
l_currentminspeed = 0
currentminspeed = -1
lastminspeed = 0
oldspeed = 0
l_currentsector = 0
currentsector = 0

def acMain(ac_version):
    global l_currentminspeed,l_steering

    appWindow = ac.newApp("minimum speed indicator")
    ac.setSize(appWindow, 200, 200)

    ac.log("Hello, Assetto Corsa application world!")
    ac.console("Hello, Assetto Corsa console!")

    l_currentminspeed = ac.addLabel(appWindow, "minspeed: 0")
    l_currentsector = ac.addLabel(appWindow, "current sector: 0")
   

    ac.setPosition(l_currentminspeed, 3, 30)
    ac.setPosition(l_currentsector, 3, 60)

    return "minimum speed indicator"
    

def acUpdate(deltaT):
    
    global l_currentminspeed,oldspeed,l_steering,currentminspeed,lastminspeed,l_currentsector,currentsector

    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    steer = ac.getCarState(0, acsys.CS.Steer)
    abs_steer = abs(steer)
    speed = int(speed)
    currentsector = info.graphics.currentSectorIndex
    ac.setText(l_currentsector, "current sector: {}".format(currentsector))

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

def acShutdown():
   # ...
   return