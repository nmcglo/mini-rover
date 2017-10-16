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

atexit.register(turnOffMotors)


#get motors
motorL = mh.getMotor(1)
motorR = mh.getMotor(2)

All = set([motorL, motorR])

def rotate(isToRight, duration):
    speed = 80
    if isToRight:
        motorR.run(BACKWARD)
    else:
        motorL.run(BACKWARD)

    motorR.setSpeed(speed)
    motorL.setSpeed(speed)
    sleep(duration)
    motorR.run(RELEASE)
    motorL.run(RELEASE)


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
        rotate(True,1)
        forward()
        sleep(1)
        rotate(False,1)
        forward()
        sleep(1)
        rotate(False,1)
        forward()
        sleep(1)
        rotate(True,1)



if __name__ == '__main__':
    main()
