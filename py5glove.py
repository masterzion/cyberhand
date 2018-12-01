'''
    File name: py5glove.py
    Author: Jairo Moreno
    Date created: 20/11/2018
    Date last modified: 02/12/2018
    Python Version: 3.6
'''

from ctypes import *

P5GLOVE_DELTA_BUTTONS=0x01
P5GLOVE_DELTA_FINGERS=0x02
P5GLOVE_DELTA_POSITION=0x04
P5GLOVE_DELTA_ROTATION=0x08

P5GLOVE_BUTTON_A=1
P5GLOVE_BUTTON_B=2
P5GLOVE_BUTTON_C=4

P5GLOVE_FINGER_INDEX=0
P5GLOVE_FINGER_MIDDLE=1
P5GLOVE_FINGER_RING=2
P5GLOVE_FINGER_PINKY=3
P5GLOVE_FINGER_THUMB=4

class P5GLOVE_POINT(Structure):
     _fields_ = ("x", c_int), ("y", c_int)

P5GLOVE_COORD_ARRAY = P5GLOVE_POINT * 3



class Glove:
    def __init__(self, index):
        self.lib=CDLL('/usr/local/lib/libp5glove.so')
        self.glove = self.lib.p5glove_open(index)

        self.lib.p5glove_sample.argtypes = [c_void_p, POINTER(c_int32)]

        self.lib.p5glove_get_finger.argtypes = [c_int]
        self.lib.p5glove_get_finger.argtypes = [c_void_p, c_int, POINTER(c_double)]

        self.lib.p5glove_get_position.argtypes = [c_void_p, P5GLOVE_COORD_ARRAY]
        self.lib.p5glove_get_rotation.argtypes = [c_void_p,  POINTER(c_double), P5GLOVE_COORD_ARRAY]
        self.lib.p5glove_get_buttons.argtypes = [c_void_p,  POINTER(c_uint32)]

        self.lib.p5glove_mouse_mode_on.argtypes = [c_void_p]
        self.lib.p5glove_mouse_mode_off.argtypes = [c_void_p]

        self.mask=0
        self.ar_rot=[]
        self.angle  = c_double()
        self.ar_fingers=[0.0, 0.0, 0.0, 0.0, 0.0]
        self.ar_coord=[]
        self.debug = False
        self.MouseMode = False

    def BeginCalibration(self):
        return self.lib.p5glove_begin_calibration(self.glove)

    def EndCalibration(self):
        return self.lib.p5glove_end_calibration(self.glove)

    def SetDebug(self, debug):
        self.debug = debug

    def GetSample(self, timeout):
        c_timeout=c_int(timeout)
        self.mask=self.lib.p5glove_sample(self.glove,c_timeout)
        return self.mask

    def GetPos(self):
        pos  = P5GLOVE_COORD_ARRAY()
        if (self.mask & P5GLOVE_DELTA_POSITION):
            self.ar_coord=[]
            if self.debug:
                print("=== POS ===")
            self.lib.p5glove_get_position(self.glove, pos)
            for pt in pos:
                self.ar_coord.append([pt.x,pt.y])
        return self.ar_coord

    def GetRotation(self):
        axis = P5GLOVE_COORD_ARRAY()
        if (self.mask & P5GLOVE_DELTA_ROTATION):
            self.ar_rot=[]
            if self.debug:
                print("=== ANGLE ===")
            self.lib.p5glove_get_rotation(self.glove, self.angle, axis)
            for pt in axis:
                self.ar_rot.append([pt.x,pt.y])
        return self.angle.value, self.ar_rot

    def GetFingers(self):
        clench = c_double(0)
        if (self.mask & P5GLOVE_DELTA_FINGERS):
            if self.debug:
                print("=== FINGERS ===")
            for x in range(5):
                self.lib.p5glove_get_finger(self.glove,x,clench)
                self.ar_fingers[x] = clench.value
        return self.ar_fingers

    def GetButtons(self):
        buttons = c_uint32()
        ar_btn=[False,False,False]

        if (self.mask & P5GLOVE_DELTA_BUTTONS):
            if self.debug:
                print("=== BUTTONS ===")
            self.lib.p5glove_get_buttons(self.glove,buttons)

            if buttons.value & P5GLOVE_BUTTON_A:
                ar_btn[0]= True
            if buttons.value & P5GLOVE_BUTTON_B:
                ar_btn[1]= True
            if buttons.value & P5GLOVE_BUTTON_C:
                ar_btn[2]= True
        return ar_btn

    def GetMouseMode(self):
        return self.MouseMode

    def SetMouseMode(self, enable):
        self.MouseMode = enable
        if enable:
            self.lib.p5glove_mouse_mode_on(self.glove)
        else:
            self.lib.p5glove_mouse_mode_off(self.glove)

    def Close(self):
        self.lib.p5glove_close(self.glove);
