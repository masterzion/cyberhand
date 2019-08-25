#!/usr/bin/python3

import mzstepper
import time

StepPins = [5,6,13,19]
interval=3500


#StepPins = [21,20,16,12]
#interval=3500

#StepPins = [4,17,27,22] 
#interval=5000


obj = mzstepper.Stepper(StepPins, 0, interval, 0.001, False)

for x in range(5):
    time.sleep(10)
    print(obj.SetPosPercent(100))
    time.sleep(10)
    print(obj.SetPosPercent(0))


