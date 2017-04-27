# -*- coding: utf-8 -*-
import socket
import time
import RPi.GPIO as GPIO
import MySQLdb
import sys
import datetime
import numpy as np
from requests_oauthlib import OAuth1Session


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


# twitter用
CK = 'kGFWP2Fm8GF4Uc2vHegxC8bEX' #consumer key
CS = 'IzV1TXgjB5rrOlV3M0Sf3Vcr91MFWo63TP7qWZPeGtH3NBC4cv' # consumer secert
AT = '479461745-xdmEVNEYpgCBtGAX1Rss7TUqYhbuqrRhzT5cWXIm' # access token
AS = 'BP8oTJf29ppq4QTNLjmSYv6kyyiNM30sWPkJHf5unKVH7' # access secret
# ツイート投稿用のURL
URL = "https://api.twitter.com/1.1/statuses/update.json"


'''
通信用だが、もう必要ないだろう
HOSTNAME = "192.168.11.254"
PORT = 12345
INTERVAL = 3
RETRYTIMES = 10
'''

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

# tweet
def tweet(text):
    #Tweetを作成
    params = {"status": text}

    # OAuth認証して、POSTで投稿
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(URL, params = params)

    #レスポンスコードを返す
    return req.status_code

counter = 0

# データベースへの接続
connector = MySQLdb.connect(host="localhost", db="pi_sensor", user="root", passwd="kiyomizu", charset="utf8")
# カーソルを取得
cursor = connector.cursor()

while(1):
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
            # データベースの日付一覧を取得
            cursor.execute('select * from temp_values')
            records = cursor.fetchall()

            d = datetime.date.today()
            cursor.execute('select * from temp_values where date = date(now())' )
            today = cursor.fetchall()
            # print(today)

            if len(today) == 0:
                # 初めての日付なら…
                # 今日の日付分を格納してhourに1を格納
                cursor.execute('insert into temp_values (date, hour) values (date(now()), 1)')
		
		# データベースを明後日、総プレイ時間を計算
		cursor.execute('select hour from temp_values')
		data = cursor.fetchall()
		# print data

		hours = np.array(data) # arrayに変形
		hours = hours[:,0] # タプルが入っているので数値だけの１次元arrayに整形
		hours = hours.astype(np.int64) # 中身をすべて整数型にキャスト
		total = hours.sum()
		# print total

		lab_minutes = (total*10)/60
		lab_hours = lab_minutes/60
		lab_minutes = lab_minutes - lab_hours*60
                print tweet('本日までのウォーリーの研究活動時間は約 %d 時間 %d 分 です。' %(lab_hours, lab_minutes))
            else :
                # すでに存在する日付なら…
                # hourだけアップデートして1追加する
                cursor.execute('update temp_values set hour = 1 + %d where date = date(now())' %(today[0][1]))


    else:
        # 指で抑えると暗くなって数値があがる
        # 要するに暗いとき
        pass
    time.sleep(10)

# database close
cursor.close()
connector.close()
