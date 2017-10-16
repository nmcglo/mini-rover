#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

from time import sleep
import atexit

FORWARD = Adafruit_MotorHAT.FORWARD
RELEASE = Adafruit_MotorHAT.RELEASE
BACKWARD = Adafruit_MotorHAT.BACKWARD

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!

motorfr = mh.getMotor(1)
motorbr = mh.getMotor(2)
motorfl = mh.getMotor(3)
motorbl = mh.getMotor(4)

Fronts = set([motorfr, motorfl])
Backs = set([motorbr, motorbl])
Lefts = set([motorfl, motorbl])
Rigths = set([motorfr, motorbr])
All = set([motorfr, motorfl, motorbr, motorbl])

myMotor = mh.getMotor(3)

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(150)
myMotor.run(Adafruit_MotorHAT.FORWARD);
# turn on motor
myMotor.run(Adafruit_MotorHAT.RELEASE);

def forward():
    print("Forward!")
    for mot in All:
        mot.run(FORWARD)

    speed = 100
    for mot in All:
        mot.setSpeed(speed)

def stop():
    print("Stop!")
    for mot in All:
        mot.run(RELEASE)

def main():
    while True:
        forward()
        sleep(1)
        stop()
        sleep(1)



if __name__ == '__main__':
    main()
