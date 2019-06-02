import Queue
import threading
import socket
import random
import time


HOST = ""
PORT = 8000

def threadWork(client):
    while True:
        msg = client.recv(1024)
        print "Client send: " + msg 
        client.send("You say: " + msg + "\r\n")
    client.close()

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print "[ERROR%d] %s\n" % (msg[0], msg[1])

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

rooms = {}

while True:
    cli_sock, addr = server.accept()
    msg = cli_sock.recv(1024)
    msg = msg.split()
    if msg[0] == "create":
        roomID = int((time.time()%10000 + random())*1000)
        rooms[roomID] = 
    if msg[0] == "join":
        roomID = msg[1]
        if rooms.has_key(msg[1]) and rooms[msg[1]].count <= 8:
            rooms[roomID].put


            new_thread = threading.Thread(target = operating_function, args = (cli_sock, addr))
            new_thread.daemon = True
            new_thread.start()
            cli_sock.sendall("OK")




server.close()