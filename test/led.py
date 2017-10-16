import RPi.GPIO as gpio
from collections import namedtuple
import colorsys
import math
import time


gpio.setmode(gpio.BCM)

def frange(start, stop, step):
    if step == 0:
        yield stop
    else:
        if start < stop:
            i = start
            while i < stop:
                yield i
                i += step
            yield stop

        elif start > stop:
            i = start
            while i > stop:
                yield i
                i -= step
            yield stop

        else:
            yield stop

    

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    if x == 0:
        return 0

class LED:

    def __init__(self, r, g, b, brightness, pins):
        self.brightness = brightness
        self.rgb = [r, g, b]
        self.pins = pins
        self.initialized = True
        self.shiftSteps = 50

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



def main():
    L1 = LED(1,0,0,100,[16,20,21,26])

    for b in range(0,2):
        for g in range(0,2):
            for r in range(0,2):
                print(r,g,b)
                L1.shiftToColor([r,g,b])
                input()

    L1.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        gpio.cleanup()