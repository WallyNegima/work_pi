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

#sql = u"insert into temp_values values(1, 5)"
#cursor.execute(sql)


while True:
    # reseive sensor data
    recvdata = conn.recv(1024)
    print "ReciveData:"+recvdata

    # データベースの日付一覧を取得
    cursor.execute('select * from temp_values')
    records = cursor.fetchall()
    #print records[0][0]
    #print records[0][1]
    #print records[0][2]


    # get time
    d = datetime.datetime.today()
    print type(d.year)
    #print 'select * from temp_values where year = %d AND month = %d AND day = %d' %(d.year, d.month, d.day)
    cursor.execute('select * from temp_values where year = %d AND month = %d AND day = %d' %(d.year, d.month, d.day))
    today = cursor.fetchall()
    print today

    if len(today) == 0:
        # 初めての日付なら…
        # 今日の日付分を格納してhourに1を格納
        cursor.execute('insert into temp_values (year, month, day, hour) values (%d, %d, %d, %d)' %(d.year, d.month, d.day, 1))
    else:
        # すでに存在する日付なら…
        # hourだけアップデートして1追加する
        cursor.execute('update temp_values set hour = %d+1 where year = %d AND month = %d AND day = %d' %(today[0][3], d.year, d.month, d.day))
        print "non null"

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
