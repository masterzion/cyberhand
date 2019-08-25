#!/usr/bin/python3

'''
    File name: cyberhand.py
    Author: Jairo Moreno
    Date created: 25/08/2019
    Date last modified: 25/08/2019
    Python Version: 3.6
'''

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
AppendStep([21,20,16,12], 3000)
AppendStep([5,5,5,5], 0) #waiting for the motor
AppendStep([5,5,5,5], 0) #waiting for the motor
AppendStep([5,6,13,19], 3000)
AppendStep([4,17,27,22], 5000)



# Disable all motors
print("== Disable all motors ==")
for i in range(5):
    arFingerMotor[i].Disable()

