## TODO:
    # **note: #! = important TODO**
#! Ensure on-board functionality
# Impliment Autoadjustment of Min/Max temp- POSSIBLE
# Determine use of map_value function
#! Adafruit has it's own library- Do the others?
#! buttonInput has no connected port. Important.
#! Determine USB file path

# Basic clock
import time

# I/O reading
import os
import fnmatch
import busio
import board
import smbus

# Data manipulation
import math
import numpy
from scipy.interpolate import griddata

# Display
import pygame as screen
from colour import Color

# Sensor Specific- Adafruit has its own library, do the others?
import adafruit_amg88xx
import MLX90640

# Define bus
i2c_bus = busio.I2C(board.SCL, board.SDA)

## Dictionary for Sensors
Sensor_Adafruit = {
    'SensorName': 'ADA'
    'SensorArray': 64
    'SensorArrayX': 8
    'SensorArrayY': 8
}
Sensor_MLX = {
    'SensorName': 'MLX'
    'SensorArray': 768
    'SensorArrayX': 32 #24 or 32?
    'SensorArrayY': 24 #24 or 32?
}
Sensor_FLIR = {
    'SensorName': 'FLIR'
    'SensorArray': 4800
    'SensorArrayX': 80
    'SensorArrayY': 60
}

##Choose from above sensors
sensor = Sensor_Adafruit
#sensor = Sensor_MLX
#sensor = Sensor_FLIR


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
#   Constraints value of color between defined bounds- Autoadjustment *is* possible, but not easy/ideal. Do anyway?
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
    
# Map Value Function
#   Functionality unknown
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def dataPoints():

    for i,j in zip(range(x),range(y))

    return pixelArray


## Thermal Variance Variabe Definition
# Likely adjust these manually later on- Range is oddly small and oddly placed.
MINTEMP = 26 #Minimum temperature, Blue
MAXTEMP = 32 #Maximum temperature, Red

COLORVARIANCE = 1024 # How many different colors can we display?


## Storage Variable Definition
# Defines the file path /dev/fb1 as arbitrary variable named SDL_FBDEV for storage use.
    #Unused?
os.putenv('SDL_FBDEV', '/dev/fb1') 
#Defines the USB file path as arbitrary variable named ScreenCap
os.putenv('ScreenCap','/media/pi/<HARD-DRIVE-LABEL>') #! Determine USB path

## Device Initialization
#Initialize screen
screen.init()

points = [(math.floor(ix / sensor['SensorArrayX']), (ix % sensor['SensorArrayY'])) for ix in range(0, sensor['SensorArray'])] # Creates array for containing SensorArray size


## 

if (sensor['SensorName'] != 'FLIR')
    grid_x, grid_y = numpy.mgrid[0:7:32j, 0:7:32j] # Creates 2 grids from 0 to 7 w/ 32 points each, including 0 & 7 as points #Requires np [32x32]
else
    grid_x, grid_y = numpy.mgrid[0:7:80j, 0:7:60j] # Prooobably wrong.

##Screen
# To adjust number of pixels on screen, adjust height, width, or displayPixelHeight or displayPixelWidth
height = 240
width = 320

displayPixelWidth = width / (width / 8)
displayPixelHeight = height / (height / 8)

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

'''
#Locate I2C active port
active = [] # Create empty array 'active'
active = [hex(x) for x in busio.I2C.scan()]

if (len(active) == 1)
    i2c_active_address = hex(busio.I2C.scan())
else
    exit() #Just close the program.
'''  

while True:

    #read the pixels
    pixelArray = [] # Creates empty array
    if sensor['SensorName'] == 'MLX'
        for row0 in range(0,24):
            for column in range(0,32):
                pixels = pixels + sensor.getCompensatedPixData(row0,column)
    else if senor['SensorName'] == 'ADA'
        for row0 in sensor['SensorName'].pixels: #Defines array as containing 'sensor' data
            pixelArray = pixelArray + row0 # Note '+' here is append, not add
    else #FLIR
        for row0 in sensor['SensorName'].pixels: #Defines array as containing 'sensor' data
            pixelArray = pixelArray + row0 # Note '+' here is append, not add
    pixelArray = [map_value(p, MINTEMP, MAXTEMP, 0, COLORVARIANCE - 1) for p in pixelArray] #Redefines 'pixels' data onto the 1024 range

    #perform interpolation
    #-> Interprets Ax^2+Bx+C line of best fit for missing data
    bicubic = griddata(points, pixelArray, (grid_x, grid_y), method='cubic')
        

    #draw everything onto screen
    for ix, row1 in enumerate(bicubic):
        for jx, pixel in enumerate(row1):
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
