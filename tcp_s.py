# -*- coding: utf-8 -*-
import socket
import MySQLdb
import sys
import datetime

HOSTNAME = "192.168.11.254"
PORT = 12345
CLIENTNUM = 3

MIN_RANGE = 8
MAX_RANGE = 50

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.bind((HOSTNAME, PORT))
s_socket.listen(CLIENTNUM)

conn, addr = s_socket.accept()
print("Conneted by"+str(addr))

# データベースへの接続
connector = MySQLdb.connect(host="localhost", db="pi_sensor", user="root", passwd="", charset="utf8")
# カーソルを取得
cursor = connector.cursor()

#sql = u"insert into temp_values values(1, 5)"
#cursor.execute(sql)


while True:
    # reseive sensor data
    recvdata = conn.recv(1024)
    print "ReciveData1:"+recvdata

    # データベースの日付一覧を取得
    cursor.execute('select * from temp_values')
    records = cursor.fetchall()

    if( recvdata != "quit"):
        temp = int(recvdata)

    if( temp <= 85):
        # 部屋が明るければ…
        # get distance
        recvdata = conn.recv(1024)
        print "ReciveData2:" + recvdata
        #get time
        d = datetime.date.today()
        # print d
        cursor.execute('select * from temp_values where date = date(now())' )
        today = cursor.fetchall()
        # print today

        if len(today) == 0 and recvdata > MIN_RANGE and recvdata < MAX_RANGE:
            # 初めての日付なら…
            # 今日の日付分を格納してhourに1を格納
            cursor.execute('insert into temp_values (date, hour) values (date(now()), %d)' %(1))
        elif recvdata > MIN_RANGE and recvdata < MAX_RANGE:
            # すでに存在する日付なら…
            # hourだけアップデートして1追加する
            cursor.execute('update temp_values set hour = %d+1 where date = date(now())' %(today[0][1]))

    if recvdata == "quit" or recvdata == "" :
        break


# database commit & close
connector.commit()
cursor.close()
connector.close()
# socket connection close
conn.close()

"""
class ConnClient(threading.Thread):

    def __init__(self,conn,addr):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.conn_socket = conn
        self.addr = addr

    def run(self):
        try:
            while (1):
                # senddata = raw_input(str(self.addr)+" SendData:")
                # self.conn_socket.send(senddata)
                recvdata = self.conn_socket.recv(1024)
                #sql = u"insert into send_data values('id1', 'recvdata')"
                #cursor.execute(sql)
                #connector.commit()
                print "ReciveData:"+recvdata
                if (recvdata == "quit"):
                    break

        except socket.error:
            print "connect error"

        finally:
            self.conn_socket.close()
            print "connect close"
            sys.exit(0)

    def stop(self):
        self.conn_socket.close()

def main():
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.bind((HOSTNAME, PORT))
        s_socket.listen(CLIENTNUM)

        # データベースへの接続
        connector = MySQLdb.connect(host="localhost", db="pi_sensor", user="root", passwd="", charset="utf8")
        # カーソルを取得
        cursor = connector.cursor()

        sql = u"insert into temp_values values(1, 5)"
        cursor.execute(sql)

        connector.commit()
        cursor.close()
        connector.close()

        while (1):
            conn, addr = s_socket.accept()
            print("Conneted by"+str(addr))
            connClientThread = ConnClient(conn,addr)
            connClientThread.setDaemon(True)
            connClientThread.start()

if __name__ == '__main__':
    main()
"""
