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


HOSTNAME = "192.168.11.254"
PORT = 12345
INTERVAL = 3
RETRYTIMES = 10

def analog_read():
    discharge()
    return charge_time()

## sensor の値取得
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

def reading(sensor):
    if sensor == 0:
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, GPIO.LOW)
        time.sleep(3)

        GPIO.output(TRIG, True)
        time.sleep(0.0001)
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

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect((HOSTNAME, PORT))

if c_socket is None:
    print "system exit:connection error"
    sys.exit(0)

print reading(0)

counter = 0
while(1):
    senddata = analog_read()
    print senddata
    #senddata = raw_input("SendData:")
    c_socket.send(str(senddata))

    if senddata > 85:
        # 指で抑えると暗くなって数値があがる
        # 要するに暗いとき
        counter = counter + 1
        time.sleep(1)
        if counter > 5:
            c_socket.send("quit")
            c_socket.close()
            break
    else:
        # 指で抑えていないときの数値
        # ようするに明るいとき
        # 部屋の普通の明るさ=25
        counter = 0
        if (senddata == "quit"):
            c_socket.close()
            break
        time.sleep(60)






"""
while True:
    print analog_read()
    time.sleep(1)

def socket_connect(host, port, interval, retries):

    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for x in range(retries):
        try:
            c_socket.connect((host, port))
            return c_socket
        except socket.error:
            print "wait"+str(interval)+"s"
            time.sleep(interval)

    c_socket.close()
    return None

def main():

    c_socket = socket_connect(HOSTNAME,PORT,INTERVAL,RETRYTIMES)

    if c_socket is None:
        print "system exit:connection error"
        sys.exit(0)

    counter = 0
    while(1):
        #recvdata = c_socket.recv(1024)
        #print "ReciveData:"+recvdata
        senddata = raw_input("SendData:")
        c_socket.send(senddata)
        counter = counter + 1
        if (senddata == "quit"):
            c_socket.close()
            break
        elif(counter > 10):
            c_socket.close()
            break

if __name__ == '__main__':
    main()
"""
