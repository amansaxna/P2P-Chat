import socket
# server won't be able to work if multiple connections try to  access simultanesously :: therefore we create threads 
import threading
import sys 
import time
from random import randint 

class Server:
    #all the connetions are stored winthin the array
    connections = []
    peers = []

    def __init__(self):
        #create a socket object
        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        #bind the socket object to an address + port
        sock.bind(('0.0.0.0', 10000))

        #open socket , listen(n) :: n = no of connection sto be allowed
        #though  never works with me it accepts more!!:>
        sock.listen(10)
        print("server running...")

        while True :
            # c:: the connection object , a :: client address 
            c , a = sock.accept()
            # after accepting the connection create a thread to handle that connection , pass the function that will handel the thread
            cThread = threading.Thread(target=self.handler , args=(c, a))
            # problem :if you close the"appending the new connection" server and if any thread is still running the os will not allow you to close
            #soclution
            cThread.daemon = True
            cThread.start()
            # do I need to explainn this!, Seriously!!
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0])+ ':' + str(a[1]) , "connected")
            #whenever someone connects send the list of peers to everyon ein the network
            self.sendPeers()

    def handler(self, c, a):
        #global connections
        while True:
            data = c.recv(1024) 
            print(str(data, 'utf-8'))
            # now to send the data back to the clients
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0])+ ':' + str(a[1]) , "dis-connected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                #when ever a peer leaves we update/send the list of peers throughout the network 
                self.sendPeers()
                break

    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p+ peer + ","
        print("server->update_overeverone(server.sendPeers)::p->")
        print(bytes(p, "utf-8"))
        # now when the peers are updated , send the list of peers
        for connection in self.connections:
            # we send an extra byte \`x11 to identify the list of peers
            connection.send(b'\x11' + bytes(p, "utf-8"))

class Client:
    
    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))
    
    def __init__(self,address):
            print("i amaamamamamamammamamamam herererererer")
            sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            sock.connect((address, 10000)) 
            # add.. = sys.argv[1]
    
            iThread = threading.Thread(target=self.sendMsg, args=(sock, )) #sends args(i.e:: sock object) in form o ftuples
            iThread.daemon = True
            iThread.start()

            while True:
                data = sock.recv(1024)
                if not data:
                    print("connected to :-----------------------------")
                    break
                #to check/differentiate b/w the peerdata vs the data check first byte[0:1] of the data
                if data[0:1] == b'\x11':
                    print("got peers")
                    print(data)
                    print("client->client.updatePeers")
                    self.updatePeers(data[1:])
                else:
                    print(str(data, 'utf-8'))
    
    def updatePeers(self , peerData):
        p2p.peers = str(peerData, "utf-8").split(",")[:-1]

#to access the peers by both the client and the server
class p2p:
    peers = ['127.0.0.1'] # set a default peer
    # (sys.argv): command line argument , if:: cjeck if there are any second command line argument(i.e the client) , ex :- python chat.py 127.0.0.01
    #if (len(sys.argv)> 1):
    #    client = Client(sys.argv[1])
    #else:
    #    server = Server()

while True:
    try:
        print("trying to connect...")
        time.sleep(randint(1,5))    
        for peer in p2p.peers:
            try:
                print("lalalalalalalaallaalalalalalalalalalal")
                print(peer)
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)  
            except:
                pass

            try:
                print("main->server()")
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0)  
            except:
                print("couldn't start the server ...")
    except KeyboardInterrupt:
        sys.exit(0)