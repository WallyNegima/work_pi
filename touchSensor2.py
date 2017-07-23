#!/usr/bin/python
# -✳- coding: utf-8 -✳- 
import os
import time
import RPi.GPIO as GPIO
import sys
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# TRIG = for distance sensor
TRIG = [19,13,6,5,11,22,27,17]
ECHO = [21,20,16,12,25,24,23,18]
DISTANCE = [0,0,0,0,0,0,0,0]

# 測距センサーで距離測定
def readDistance(sensor):
    if sensor >= 0:
        signaloff = [0,0,0,0]
        signalon = [0,0,0,0]
        for i in range(4):
            GPIO.output(TRIG[sensor+(i*2)], True)
            time.sleep(0.00001)
            GPIO.output(TRIG[sensor+(i*2)], False)
            while GPIO.input(ECHO[sensor+i*2]) == 0:
                signaloff[i] = time.time()

        for i in range(4):
            while GPIO.input(ECHO[sensor+i*2]) == 1:
                signalon[i] = time.time()

        for i in range(4):
            DISTANCE[sensor+i*2] = (signalon[i] - signaloff[i])*17000
            print '%d' %DISTANCE[sensor+i*2]

        #timepassed = signalon - signaloff
        #distance = timepassed * 17000
        #return distance
       # GPIO.cleanup()
    else:
        print "Incorrect usonic() function variable"

def main():
  print "start!"
  for i in range(8):
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)
    GPIO.output(TRIG[i], GPIO.LOW)
    time.sleep(0.2)

  while(1):
    DISTANCE = [0,0,0,0,0,0,0,0]
    for i in range(2):
      readDistance(i)
      #for j in range(4):
       # print '%d' %DISTANCE[i+j*2]
      time.sleep(0.01)
    print "-----------"

if __name__ == "__main__":
  main()
