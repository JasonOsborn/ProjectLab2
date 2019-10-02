"""This example is for Raspberry Pi (Linux) only!
   It will not work on microcontrollers running CircuitPython!"""
#!/usr/bin/env python3

import os
import math
import time
import datetime
import busio
import board
import sys

#from signal import pause

import numpy as np
import pygame
from scipy.interpolate import griddata

from colour import Color
import RPi.GPIO as GPIO
import adafruit_amg88xx

#GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)

i2c_bus = busio.I2C(board.SCL, board.SDA)

#low range of the sensor (this will be blue on the screen)
MINTEMP = 26.

#high range of the sensor (this will be red on the screen)
MAXTEMP = 28.

#how many color values we can have
COLORDEPTH = 1024

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

#initialize the sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

# pylint: disable=invalid-slice-index
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j] #0:7:32 original
# pylint: enable=invalid-slice-index

#sensor is an 8x8 grid so lets do a square
height = 420#240x240 original
width = 640 #pygame window size

#the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

displayPixelWidth = width / 20 #30 original
displayPixelHeight = height / 20 #30 original

lcd = pygame.display.set_mode((width, height))

lcd.fill((255, 0, 0)) #255 orginal

pygame.display.update()
pygame.mouse.set_visible(False)

lcd.fill((0, 0, 0))
pygame.display.update()

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#let the sensor initialize
time.sleep(.1)
 
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
    
    if(GPIO.input(17) == 0):
        now = datetime.datetime.now()#displays cur time
        str_now = str(now)
        d_str = str_now[5:10]
        d_str1 = str_now[11:19]#f_date displays m-d_h-m-s time
        f_date = d_str+"_"+d_str1[0:2]+"-"+d_str1[3:5]+\
                 "-"+d_str1[6:8]
        image_file = "scrot /media/pi/5BD7-E1141/sample"\
                     +f_date+".png"    
        os.system(image_file)
        
        print("f_date = ")
        print(f_date)
        print(str_now)
    if(GPIO.input(23) == 0):
        sys.exit()