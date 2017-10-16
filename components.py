import RPi.GPIO as gpio
from collections import namedtuple
import colorsys
import math
import time
from util import frange
from util import sign
import threading

class LED:

    def __init__(self, r, g, b, brightness, pins):
        self.brightness = brightness
        self.rgb = [r, g, b]
        self.pins = pins
        self.initialized = True
        self.shiftSteps = 50
        self.lock = threading.Lock()

        # Setup all the LED colors with an initial
        # duty cycle of 100 which is off
        gpio.setup(pins[0],gpio.OUT)
        gpio.setup(pins[1],gpio.OUT)
        gpio.setup(pins[2],gpio.OUT)
        gpio.setup(pins[3], gpio.OUT)

        gpio.output(pins[3],1)

        
        Freq = 120 #Hz
        RED = gpio.PWM(pins[0], Freq)
        RED.start(100)
        GREEN = gpio.PWM(pins[1], Freq)
        GREEN.start(100)
        BLUE = gpio.PWM(pins[2], Freq)
        BLUE.start(100)

        PinObjects = namedtuple('PinObjects', ['RED', 'GREEN','BLUE'])
        self.pinObjs = PinObjects(RED,GREEN,BLUE)

    def reInit(self):
        if not self.initialized:
            # Setup all the LED colors with an initial
            # duty cycle of 100 which is off
            gpio.setup(self.pins[0],gpio.OUT)
            gpio.setup(self.pins[1],gpio.OUT)
            gpio.setup(self.pins[2],gpio.OUT)
            gpio.setup(self.pins[3], gpio.OUT)

            gpio.output(self.pins[3],1)
            
            Freq = 120 #Hz
            RED = gpio.PWM(self.pins[0], Freq)
            RED.start(100)
            GREEN = gpio.PWM(self.pins[1], Freq)
            GREEN.start(100)
            BLUE = gpio.PWM(self.pins[2], Freq)
            BLUE.start(100)

            PinObjects = namedtuple('PinObjects', ['RED', 'GREEN','BLUE'])
            self.pinObjs = PinObjects(RED,GREEN,BLUE)

            self.on = True
            self.setColor(self.rgb)

    def setBrightness(self,newBrightness):
        self.brightness = newBrightness


    def setPins(self, newPins):
        self.pins = newPins

    def setColor(self, newColor):
        self.rgb = newColor
        self.pinObjs.RED.ChangeDutyCycle(100-(self.rgb[0]*self.brightness))
        self.pinObjs.GREEN.ChangeDutyCycle(100-(self.rgb[1]*self.brightness))
        self.pinObjs.BLUE.ChangeDutyCycle(100-(self.rgb[2]*self.brightness))

    def shiftToColor(self, newColor):
        curValues = self.rgb

        diffs = [abs(newColor[i] - curValues[i]) for i in range(3)]

        for i in range(len(diffs)):
            diffs[i] = round(diffs[i]*1000)/1000

        shiftVals = [0,0,0]
        for c in range(3):
            if(diffs[c] != 0):
                shiftVals[c] = [i for i in frange(curValues[c], newColor[c], diffs[c]/self.shiftSteps)]
            else:
                shiftVals[c] = [self.rgb[c]] * (self.shiftSteps+1)

        shiftr = shiftVals[0]
        shiftg = shiftVals[1]
        shiftb = shiftVals[2]        

        for s in range(self.shiftSteps+1):
            shiftr[s] = round(shiftr[s]*1000)/1000
            shiftg[s] = round(shiftg[s]*1000)/1000
            shiftb[s] = round(shiftb[s]*1000)/1000

            self.setColor([shiftr[s], shiftg[s], shiftb[s]])
            time.sleep(.003)

    
    def cleanup(self):
        gpio.cleanup(self.pins)


class DistanceSensor:

    def __init__(self,trigPin, echoPin):
        self.triggerPin = trigPin
        self.echoPin = echoPin
        gpio.setup(self.triggerPin, gpio.OUT)
        gpio.setup(self.echoPin, gpio.IN)
        self.lock = threading.Lock()

    def distance(self):
            # set Trigger to HIGH
            gpio.output(self.triggerPin, True)

            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            gpio.output(self.triggerPin, False)

            StartTime = time.time()
            StopTime = time.time()

            # save StartTime
            while gpio.input(self.echoPin) == 0:
                StartTime = time.time()

            # save time of arrival
            while gpio.input(self.echoPin) == 1:
                StopTime = time.time()

            TimeElapsed = StopTime - StartTime
            distance = (TimeElapsed * 34300) / 2

            return distance

    def cleanup(self):
        gpio.cleanup([self.echoPin,self.triggerPin])


#