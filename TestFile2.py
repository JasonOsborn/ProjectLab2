## TODO:
# Ensure on-board functionality
# Impliment Autoadjustment of Min/Max temp- POSSIBLE
# Determine use of map_value function

import os
import math
import time

import busio
import board

import numpy
import pygame as screen
from scipy.interpolate import griddata
from colour import Color

# Sensor Specific- Adafruit has its own library, do the others?
import adafruit_amg88xx

i2c_bus = busio.I2C(board.SCL, board.SDA)

##Define Custom Functions
# Constrain Function
#   Constraints value of temperature/color between defined bounds- Autoadjustment *is* possible, but not easy/ideal. Do anyway?
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
    
# Map Value Function
#   Functionality unknown
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

## Thermal Variance Variabe Definition
# Likely adjust these manually later on- Range is oddly small and oddly placed.
MINTEMP = 26 #Minimum temperature, Blue
MAXTEMP = 32 #Maximum temperature, Red

COLORVARIANCE = 1024 # How many different colors can we display?

## Storage Variable Definition
#Defines the file path /dev/fb1 as arbitrary variable named SDL_FBDEV for storage use.
os.putenv('SDL_FBDEV', '/dev/fb1') 

## Device Initialization
#Initialize screen
screen.init()

#initialize sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)


##Define sensor's output array
SensorArray = 768    ## REDEFINE for each sensor. 
# adafruit: (x=8)*(y=8) = 64
# sensor 2: (x=32)*(y=24) = 768
#sensor 3: ?

SensorArrayX = SensorArray / 24  ## REDEFINE in terms of sensor's array X size, noted above.
SensorArrayY = SensorArray / 32  ## REDEFINE in terms of sensor's array Y size, noted above.

points = [(math.floor(ix / SensorArrayX), (ix % SensorArrayY)) for ix in range(0, SensorArray)] # Creates array for containing SensorArray size


## 
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j] # Creates 2 grids from 0 to 7 w/ 32 points each, including 0 & 7 as points #Requires np


