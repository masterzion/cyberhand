import mzstepper
import time

#StepPins = [5,6,13,19]
StepPins = [21,20,16,12]
#StepPins = [4,17,27,22]


obj = mzstepper.Stepper(StepPins, 0, 2000, 0.1, True)

for x in range(5):
    time.sleep(0.1)
    print(obj.SetPosPercent(90) )
    time.sleep(3)
    print(obj.SetPosPercent(20) )
obj.Disable()
