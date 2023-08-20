import sys
import os
import platform
if platform.architecture()[0] == "64bit":
    dllfolder = "third_party\stdlib64"
else:
    dllfolder = "third_party\stdlib"
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(cwd, dllfolder))

import time

from sim_info import info

while True:
    asd = info.graphics.tyreCompound
    print(asd)
    time.sleep(1)