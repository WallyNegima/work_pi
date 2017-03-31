import socket
import threading
import time

HOSTNAME = "192.168.11.254"
PORT = 12345
CLIENTNUM = 3

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
                sql = u"insert into send_data values('id1', 'recvdata');
                cursor.execute(sql)
                connector.commit()
                print "ReciveData:"+recvdata
                if (recvdata == "quit"):
                    break

        except socket.error:
            print "connect error"

        finally:
            self.conn_socket.close()
            print "connect close"

    def stop(self):
        self.conn_socket.close()

def main():
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.bind((HOSTNAME, PORT))
        s_socket.listen(CLIENTNUM)

        while (1):
            conn, addr = s_socket.accept()
            print("Conneted by"+str(addr))
            connClientThread = ConnClient(conn,addr)
            connClientThread.setDaemon(True)
            connClientThread.start()

if __name__ == '__main__':
    connector = MySQLab.connect(host="localhost", db="s_test", user="root", passwd="", charset="utf8")
    cursor = connector.cursor()
    main()
