## TODO:
    # **note: #! = important TODO**
#! Ensure on-board functionality
# Impliment Autoadjustment of Min/Max temp- POSSIBLE
# Determine use of map_value function
#! Adafruit has it's own library- Do the others?
#! buttonInput has no connected port. Important.

# Basic clock
import time

# I/O reading
import os
import fnmatch
import busio
import board

# Data manipulation
import math
import numpy
from scipy.interpolate import griddata

# Display
import pygame as screen
from colour import Color

# Sensor Specific- Adafruit has its own library, do the others?
import adafruit_amg88xx

# Define bus
i2c_bus = busio.I2C(board.SCL, board.SDA)


## Dictionary for Sensors
Sensor_Adafruit = {
    'SensorName': adafruit_amg88xx.AMG88XX(i2c_bus)
    'SensorArray': 64
    'SensorArrayX': 8
    'SensorArrayY': 8
}
Sensor_2 = {
    'SensorName': '0'
    'SensorArray': 768
    'SensorArrayX': 8
    'SensorArrayY': 8
}
Sensor_3 = {
    'SensorName': '0'
    'SensorArray': 0
    'SensorArrayX': 0
    'SensorArrayY': 0
}

##Define Custom Functions
# Number Function
#   Locates the first unused Image file name in format "image[Num].jpg" where Num is an arbitrary interger
def Numbr(USB_Path)
    Num = 0
    listFiles = os.listdir(USB_Path)
    if len(listFiles) == 0:
        return 0
    else
        for fileName in listFiles:
            if not(fnmatch.fnmatch(fileName, "image" + str(Num) + ".jpg")):
                return Num
            else
                Num = Num + 1
    return 0

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
MINTEMP_T = 26 #Minimum temperature, Blue
MAXTEMP_T = 32 #Maximum temperature, Red
MINTEMP = MINTEMP_T
MAXTEMP = MAXTEMP_T

COLORVARIANCE = 1024 # How many different colors can we display?

## Storage Variable Definition
# Defines the file path /dev/fb1 as arbitrary variable named SDL_FBDEV for storage use.
    #Unused?
os.putenv('SDL_FBDEV', '/dev/fb1') 
#Defines the USB file path as arbitrary variable named ScreenCap
os.putenv('ScreenCap','')

## Device Initialization
#Initialize screen
screen.init()

#Choose sensor
sensor = Sensor_Adafruit

points = [(math.floor(ix / sensor['SensorArrayX']), (ix % sensor['SensorArrayY'])) for ix in range(0, sensor['SensorArray'])] # Creates array for containing SensorArray size


## 
grid_x, grid_y = numpy.mgrid[0:7:32j, 0:7:32j] # Creates 2 grids from 0 to 7 w/ 32 points each, including 0 & 7 as points #Requires np


##Screen
# To adjust number of pixels on screen, adjust height, width, or displayPixelHeight or displayPixelWidth
height = 240
width = 240

displayPixelWidth = width / 30
displayPixelHeight = height / 30

#Colors for the screen, from blue('indigo') to red. Number of jumps between is COLORVARIANCE

colors = list(Color("indigo").range_to(Color("red"), COLORVARIANCE)) # list of all colors btwn blue and red

#Redefines 'colors' into accessible RGB format
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors] # Redefines array colors in terms of RGB screen codes


# Boot commands for the screen
LiveCap = screen.display.set_mode((width, height))
 
LiveCap.fill((255, 0, 0))
 
screen.display.update()
screen.mouse.set_visible(False)
 
LiveCap.fill((0, 0, 0))
screen.display.update()

time.sleep(.1)

# Initialize 
Num = Numbr(ScreenCap)
t0 = 0

while True:
    
    MAXTEMP = MAXTEMP_T
    MINTEMP = MINEMP_T
    #read the pixels
    pixels = [] # Creates empty array
    for row in sensor['SensorName'].pixels: #Defines array as containing 'sensor' data
        pixels = pixels + row
    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORVARIANCE - 1) for p in pixels] #Redefines 'pixels' data onto the 1024 range

    #perform interpolation
    #-> Interprets Ax^2+Bx+C line of best fit for missing data
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')

    #draw everything onto screen
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            screen.draw.rect(LiveCap, colors[constrain(int(pixel), 0, COLORVARIANCE - 1)],
                             (displayPixelHeight * ix, displayPixelWidth * jx,
                              displayPixelHeight, displayPixelWidth))

    screen.display.update()

    ## Screenshot functionality
    # Debouncing + Initial Button Input:
    t1 = time.clock() - t0
    if buttonInput and t1 > 0.3:
        t0 = time.clock()
        # Save a screenshot of the current screen @ ScreenCap called image[Num].jpg where Num is an arbitrary number
        screen.image.save(LiveCap, ScreenCap + "image" + str(Num) + ".jpg")
        Num = Num + 1   
#End
