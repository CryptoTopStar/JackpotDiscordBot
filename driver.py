## run the script in commands.py in a command line
## every 20 seconds, terminate the script and run it again

import os
import sys
import time
import signal
import subprocess as sp


PATH = "./Cache/missions.json"
extProc = sp.Popen(['python3','commands.py'])
lastMod = os.path.getmtime(PATH)
## Execute only if the file has been changed
while True:
    if lastMod != os.path.getmtime(PATH):
        time.sleep(40)
        lastMod = os.path.getmtime(PATH)
        sp.Popen.terminate(extProc)
        extProc = sp.Popen(['python3','commands.py'])
    else:
        time.sleep(10)