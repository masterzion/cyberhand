'''
    File name: cyberhand.py
    Author: Jairo Moreno
    Date created: 21/11/2018
    Date last modified: 21/11/2018
    Python Version: 3.6
'''

import py5glove
import mzstepper
import time


#init vars
ar_fingers = [0.0, 0.0, 0.0, 0.0, 0.0]
arFingerMotor = []

#Add mechanical finger object
def AppendStep(StepPins, size):
    interval = 0.001
    return arFingerMotor.append(mzstepper.Stepper(StepPins, 0, size, interval, False, False))

# control motor for each finger
AppendStep([21,20,16,12], 5000)
AppendStep([5,5,5,5], 0) #waiting for the motor
AppendStep([5,5,5,5], 0) #waiting for the motor
AppendStep([5,6,13,19], 5000)
AppendStep([4,17,27,22], 10000)



# Disable all motors
print("== Disable all motors ==")
print("Please adjust the strings manually")
for i in range(5):
    arFingerMotor[i].Disable()

# start glove and begin glove calibration
obj = py5glove.Glove(-1)
print("1) Press button B on the glove")
print("2) Close your hand a few times")
print("3) Open your hand")
print("4) Press button C on the glove")

while True:
    obj.GetSample(-1)
    ar = obj.GetButtons()
    time.sleep(0.01)
    print(ar)
    if ar[1]:
        break

time.sleep(3)

print("== BeginCalibration ==")
obj.BeginCalibration()
while True:
    obj.GetSample(-1)
    time.sleep(0.1)
    print(ar)
    ar = obj.GetButtons()
    if ar[2]:
        break
obj.EndCalibration()

print("== EndCalibration ==")

time.sleep(3)

print("== Begin Loop ==")
while True:
    obj.GetSample(-1)
    ar_f_finger = obj.GetFingers()
    print(ar_f_finger)
    for i in range(0, 5):
        arFingerMotor[i].SetPosPercent(int(ar_f_finger[i] * 10)*10)
    time.sleep(0.1)
