import socket
import time
import select
import sys
import Players
from Players import Player
import json
import traceback

delay = 0
buff_size = 6096
clients = dict() 

class Server:
    def __init__(self, host, port):
        self.list = [] #contains all client sockets
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))

        print 'Server ready...'
        self.server.listen(5)
        self.data = None #data being sent by client

    def main(self):
        self.list.append(self.server)
        while True:
            #select() will choose a client socket to read
            input_, output_, except_ = select.select(self.list, [], [])

            for self.s in input_:
                #Connect to chosen client socket
                if self.s == self.server: 
                    remote_socket, addr = self.server.accept() 
                    print str(addr) + ' connected.'
                    clients[addr[1]] = [] 
                    self.list.append(remote_socket) 
                    break
                else:
                    #recieve data from selected client in input_
                    self.data = self.s.recv(buff_size)
                if self.data == "None":
                    #getpeername() -> gets name of socket server is connected to (addr)
                    peer_addr = self.s.getpeername()[1] 
                    clients[peer_addr] = self.data
                    self.s.send(json.dumps(clients))
                    del(clients[peer_addr])
                    self.list.remove(self.s)
                    print peer_addr, " has disconnected"
                else:
                    #sends dictionary of clients = {client_addr : data}
                    peer_addr = self.s.getpeername()[1]
                    clients[peer_addr] = json.loads(self.data)
                    self.s.send(json.dumps(clients))
                    
try:
    server = Server('127.0.0.1', 6961)
    server.main()

except KeyboardInterrupt:
    print 'Interrupted'
    sys.exit(1)
                    
