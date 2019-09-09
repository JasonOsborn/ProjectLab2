import os
import math
import time


import busio
import board
 
import numpy as np
import pygame
from scipy.interpolate import griddata
 
from colour import Color

#import adafruit_amg88xx
 
i2c_bus = busio.I2C(board.SCL, board.SDA)


# Define new functions:

# When given an actual value and its maximum and minimum possible values, returns value unless outside bounds, where it returns closer bound.
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

# ??
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


MINTEMP = 26 # Blue

MAXTEMP = 32 # Red

COLORVARIANCE = 1024 # Number of color values


os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

""" 
#initialize the sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)
"""

points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)] # Creates 8x8 (?) array

grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j] # Creates 2 grids from 0 to 7 w/ 32 points each, including 0 & 7 as points #Requires np


# Screen
height = 240
width = 240

displayPixelWidth = width / 30
displayPixelHeight = height / 30

#Colors for the screen, from blue('indigo') to red

colors = list(Color("indigo").range_to(Color("red"), COLORVARIANCE)) # requires color

#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors] # Redefines array colors in terms of RGB screen codes



# Setup commands for the screen
lcd = pygame.display.set_mode((width, height))
 
lcd.fill((255, 0, 0))
 
pygame.display.update()
pygame.mouse.set_visible(False)
 
lcd.fill((0, 0, 0))
pygame.display.update()


time.sleep(.1)


# Prints thermal image to screen

while True:
 
    #read the pixels
    pixels = []
    for row in sensor.pixels:
        pixels = pixels + row
    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
 
    #perform interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
 
    #draw everything
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)],
                             (displayPixelHeight * ix, displayPixelWidth * jx,
                              displayPixelHeight, displayPixelWidth))
 
    pygame.display.update()


print("End")
