'''
    File name: test.py
    Author: Jairo Moreno
    Date created: 20/11/2018
    Date last modified: 20/11/2018
    Python Version: 3.6
'''

import py5glove
import time

obj = py5glove.Glove(-1)
while True:
    obj.GetSample(-1)
    print("GetFingers")
    print( obj.GetFingers() )
    print("GetButtons")
    print( obj.GetButtons() )
    print("GetPos")
    print( obj.GetPos() )
    print("GetRotation")
    print( obj.GetRotation() )
    time.sleep(0.1)
