# -*- coding: utf-8 -*-
import socket
import MySQLdb
import sys
import datetime

HOSTNAME = "192.168.11.254"
PORT = 12345
CLIENTNUM = 3

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
print today

if len(today) == 0:
    # 初めての日付なら…
    # 今日の日付分を格納してhourに1を格納
    cursor.execute('insert into temp_values (date, hour) values (date(now()), %d)' %(int(recvdata)))
else :
    # すでに存在する日付なら…
    # hourだけアップデートして1追加する
    cursor.execute('update temp_values set hour = hour + %d where date = date(now())' %(int(recvdata)))


# database commit & close
connector.commit()
cursor.close()
connector.close()
# socket connection close
conn.close()
