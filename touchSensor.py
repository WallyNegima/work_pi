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

# 測距センサーで距離測定
def readDistance(sensor, trig, echo):
    if sensor >= 0:
#        print('%d' %sensor)
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
        print "Incorrect usonic() function variable"

def main():
  print "start!"
  for i in range(8):
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)
    GPIO.output(TRIG[i], GPIO.LOW)
    time.sleep(0.2)

  while(1):
    for i in range(8):
      distance = readDistance(i, TRIG[i], ECHO[i])
      print(distance)
      time.sleep(0.01)
    print "-----------"

if __name__ == "__main__":
  main()
