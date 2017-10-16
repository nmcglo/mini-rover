#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  RGB_LED.py
#
# A short program to control an RGB LED by utilizing
# the PWM functions within the Python GPIO module
#
#  Copyright 2015  Ken Powers
#   
 
# Import the modules used in the script
import random, time
import colorsys
import RPi.GPIO as GPIO
 
# Set GPIO to Broadcom system and set RGB Pin numbers
RUNNING = True
GPIO.setmode(GPIO.BCM)
red = 16
green = 20
blue = 21
on = 26
 
# Set pins to output mode
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(on, GPIO.OUT)

GPIO.output(on,1)

 
Freq = 120 #Hz
 
# Setup all the LED colors with an initial
# duty cycle of 0 which is off
RED = GPIO.PWM(red, Freq)
RED.start(100)
GREEN = GPIO.PWM(green, Freq)
GREEN.start(100)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(100)
 
# Define a simple function to turn on the LED colors
def color(R, G, B, on_time):
    # Color brightness range is 0-100%
    RED.ChangeDutyCycle(100-R)
    GREEN.ChangeDutyCycle(100-G)
    BLUE.ChangeDutyCycle(100-B)
    time.sleep(on_time)
 
    # Turn all LEDs off after on_time seconds
    # RED.ChangeDutyCycle(100)
    # GREEN.ChangeDutyCycle(100)
    # BLUE.ChangeDutyCycle(100)
 
print("Light It Up!")
print("Press CTRL + C to quit.\n")
print(" R  G  B\n---------")

try:
    while RUNNING:
        for h in range(0,1001):
            nextColor = colorsys.hsv_to_rgb(h/1000.0,1.0,1.0)
            print(h/1000.0, '==', nextColor)
            color(nextColor[0]*100, nextColor[1]*100, nextColor[2]*100,0.005)
    


# except KeyboardInterrupt
#     pass

# # Main loop
# try:
#     while RUNNING:
#         for x in range(0,2):
#             for y in range(0,2):
#                 for z in range(0,2):
#                     print (x,y,z)
#                     # RED.ChangeDutyCycle(100-(x*100))
#                     # GREEN.ChangeDutyCycle(100-(y*100))
#                     # BLUE.ChangeDutyCycle(100-(z*100))
#                     # input()

#                     # Slowly ramp up power percentage of each active color
#                     for i in (range(0,101)):
#                         color((x*i),(y*i),(z*i), .01)

# If CTRL+C is pressed the main loop is broken
except KeyboardInterrupt:
    RUNNING = False
    print("\Quitting")
 
# Actions under 'finally' will always be called
# regardless of what stopped the program
finally:
    # Stop and cleanup so the pins
    # are available to be used again
    GPIO.cleanup()