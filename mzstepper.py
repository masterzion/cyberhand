'''
    File name: mzstepper.py
    Author: Jairo Moreno
    Date created: 20/11/2018
    Date last modified: 22/11/2018
    Python Version: 3.6

    Based on: https://www.raspberrypi-spy.co.uk/2012/07/stepper-motor-control-in-python/
'''

# Import required libraries
import sys
import time
import _thread
import RPi.GPIO as GPIO


SeqDef =  [[1,0,0,1],
           [1,0,0,0],
           [1,1,0,0],
           [0,1,0,0],
           [0,1,1,0],
           [0,0,1,0],
           [0,0,1,1],
           [0,0,0,1]]

class Stepper:
    def __init__(self, StepPins, CurrentPos = 0, MaxStep = 2000, WaitTime = 0.5, Debug = False, TurnOff = True, Seq = SeqDef ):
        self.MaxStep = MaxStep
        self.CurrentPos = CurrentPos
        self.NewPos = CurrentPos
        self.WaitTime = WaitTime
        self.StepPins = StepPins
        self.Seq = Seq
        self.TurnOff = TurnOff
        self.Debug = Debug

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in self.StepPins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        self.thread = _thread.start_new_thread(self.MoveMotor, () )

    def GetThread(self):
        return self.thread



    def SetPosPercent(self, NewPosPercent):
        return self.SetPos( int(self.MaxStep  / 100 * float(NewPosPercent)) )


    def SetPos(self, NewPos):
        if self.NewPos > self.MaxStep:
            return False

        if self.NewPos < 0 :
            return False

        self.NewPos = NewPos

    def GetPos(self):
        return self.CurrentPos


    def MoveMotor(self):

        # Initialise variables
        StepCounter = 0
        StepCount = len(self.Seq)
        pin_len=len(self.Seq[0])

        # Start main loop
        while True:
            # Wait before moving on
            time.sleep(self.WaitTime)

            if self.NewPos == self.CurrentPos:
                if self.TurnOff:
                    self.Disable()
            else:
                if self.NewPos < self.CurrentPos :
                    StepDir = -1
                else:
                    StepDir = 1

                if self.Debug:
                    print("StepCounter: "+str(StepCounter) )
                    print(self.Seq[StepCounter])

                for pin in range(0, pin_len):
                    xpin = self.StepPins[pin]
                    if self.Seq[StepCounter][pin]!=0:
                        if self.Debug:
                            print(str(self.CurrentPos) + " Enable GPIO %i"  %(xpin))
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)

                StepCounter += StepDir
                self.CurrentPos += StepDir

                # If we reach the end of the sequence
                # start again
                if (StepCounter>=StepCount):
                    StepCounter = 0
                if (StepCounter<0):
                    StepCounter = StepCount+StepDir
        return True

    def Disable(self):
        for pin in self.StepPins:
            if self.Debug:
                print("disable pins")
            GPIO.output(pin, False)
