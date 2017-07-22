#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO
import sys
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# TRIG = for distance sensor
TRIG = [17,27,22,11,5,6,13,19]
ECHO = [18,23,24,25,12,16,20,21]

# 測距センサーで距離測定
def readDistance(sensor, trig, echo):
    if sensor == 0:
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        GPIO.output(trig, GPIO.LOW)
        time.sleep(0.2)

        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        while GPIO.input(echo) == 0:
            signaloff = time.time()

        while GPIO.input(echo) == 1:
            signalon = time.time()

        timepassed = signalon - signaloff
        distance = timepassed * 17000
        return distance
        GPIO.cleanup()
    else:
        print("Incorrect usonic() function variable")

def main():
  while ture:
    distance = readDistance(0, TRIG[0], ECHO[0])
    print(distance)
    time.sleep(1000)

if __name__ == "__main__":
  main()