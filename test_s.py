# -*- coding: utf-8 -*-
import socket
import MySQLdb
import sys
import datetime
import numpy as np
from requests_oauthlib import OAuth1Session

HOSTNAME = "192.168.11.254"
PORT = 12345
CLIENTNUM = 3

CK = 'kGFWP2Fm8GF4Uc2vHegxC8bEX' #consumer key
CS = 'IzV1TXgjB5rrOlV3M0Sf3Vcr91MFWo63TP7qWZPeGtH3NBC4cv' # consumer secert
AT = '479461745-xdmEVNEYpgCBtGAX1Rss7TUqYhbuqrRhzT5cWXIm' # access token
AS = 'BP8oTJf29ppq4QTNLjmSYv6kyyiNM30sWPkJHf5unKVH7' # access secret
# ツイート投稿用のURL
URL = "https://api.twitter.com/1.1/statuses/update.json"

def tweet(text):
    #Tweetを作成
    params = {"status": text}

    # OAuth認証して、POSTで投稿
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(URL, params = params)

    #レスポンスコードを返す
    return req.status_code

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.bind((HOSTNAME, PORT))
s_socket.listen(CLIENTNUM)

conn, addr = s_socket.accept()
print("Conneted by"+str(addr))

# データベースへの接続
connector = MySQLdb.connect(host="localhost", db="pi_sensor", user="root", passwd="", charset="utf8")
# カーソルを取得
cursor = connector.cursor()

# reseive sensor data
recvdata = conn.recv(1024)
print "ReciveData:"+recvdata

# データベースの日付一覧を取得
cursor.execute('select * from temp_values')
records = cursor.fetchall()


d = datetime.date.today()
cursor.execute('select * from temp_values where date = date(now())' )
today = cursor.fetchall()

#print tweet(recvdata)

if len(today) == 0:
    # 初めての日付なら…
    # 今日の日付分を格納してhourに1を格納
    cursor.execute('insert into temp_values (date, hour) values (date(now()), %d)' %(int(recvdata)))
else :
    # すでに存在する日付なら…
    # hourだけアップデートして1追加する
    cursor.execute('update temp_values set hour = hour + %d where date = date(now())' %(int(recvdata)))

# データベースを明後日、総プレイ時間を計算
cursor.execute('select hour from temp_values')
data = cursor.fetchall()
print data

hours = np.array(data) # arrayに変形
hours = hours[:,0] # タプルが入っているので数値だけの１次元arrayに整形
hours = hours.astype(np.int64) # 中身をすべて整数型にキャスト
total = hours.sum()
print total

lab_minutes = (total*10)/60
lab_hours = lab_minutes/60
lab_minutes = lab_minutes - lab_hours*60
print '本日までのウォーリーの研究活動時間は約 %d 時間 %d 分 です。' %(lab_hours, lab_minutes)

# database commit & close
connector.commit()
cursor.close()
connector.close()
# socket connection close
conn.close()
