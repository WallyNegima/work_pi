# -*- coding: utf-8 -*-
import socket
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# a & b pin = for photo sensor
a_pin = 18
b_pin = 23
# TRIG = for distance sensor
TRIG = 27
ECHO = 22

# 測距センサーのしきい値
MIN_RANGE = 9
MAX_RANGE = 50

HOSTNAME = "192.168.11.254"
PORT = 12345
INTERVAL = 3
RETRYTIMES = 10

##   光sensor の値取得
def analog_read():
    discharge()
    return charge_time()

def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.005)

def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    count = 0
    GPIO.output(a_pin, True)
    while not GPIO.input(b_pin):
        count = count + 1
    return count

# 測距センサーで距離測定
def reading(sensor):
    if sensor == 0:
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, GPIO.LOW)
        time.sleep(0.3)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            signaloff = time.time()

        while GPIO.input(ECHO) == 1:
            signalon = time.time()

        timepassed = signalon - signaloff
        distance = timepassed * 17000
        return distance
        GPIO.cleanup()
    else:
        print "Incorrect usonic() function variable"

counter = 0
while(1):
    # 接続を試みる
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 接続できたら送信
        c_socket.connect((HOSTNAME, PORT))
        c_socket.send(str(counter))
        counter = 0
        c_socket.shutdown(1)
        c_socket.close()
    except socket.error:
        # 接続できなければ1秒まってセンシング再開
        time.sleep(1)

    # 光度取得
    temp = analog_read()
    print temp

    if int(temp) < 40:
        # 指で抑えていないときの数値
        # ようするに明るいとき
        # 部屋の普通の明るさ=25

        # 距離取得
        distance = reading(0)
        print distance

        time.sleep(1)
        if float(distance) > MIN_RANGE and float(distance) < MAX_RANGE:
            counter = counter + 1
    else:
        # 指で抑えると暗くなって数値があがる
        # 要するに暗いとき
        pass
    time.sleep(10)
