## run the script in commands.py in a command line
## every 20 seconds, terminate the script and run it again

import os
import sys
import time
import signal
import subprocess as sp

PATH = "./Cache/missions.json"
PATH2 = "./Cache/Objects/SERVER_NAMES.json"
extProc = sp.Popen(['python3','commands.py'])
lastMod = os.path.getmtime(PATH)
lastMod2 = os.path.getmtime(PATH2)
counter = 1

## Execute only if the file has been changed
while True:
    if lastMod != os.path.getmtime(PATH) or lastMod2 != os.path.getmtime(PATH2) or counter % 10000 == 0:
        extProc.kill()
        lastMod = os.path.getmtime(PATH)
        lastMod2 = os.path.getmtime(PATH2)
        sp.Popen.terminate(extProc)
        extProc = sp.Popen(['python3','commands.py'])
        counter = 1
        time.sleep(10)
    else:
        time.sleep(10)
        counter += 1