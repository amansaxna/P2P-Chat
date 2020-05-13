import socket
# server won't be able to work if multiple connections try to  access simultanesously :: therefore we create threads 
import threading
import sys 
import time
from random import randint 
from blockchain import Blockchain 

class Server:
    #all the connetions are stored winthin the array
    connections = []
    peers = []

    def __init__(self, chain):
        self.chain = chain
        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock.bind(('0.0.0.0', 10000))
        sock.listen(10)
        print("server running...")

        while True :
            # c:: the connection object , a :: client address 
            c , a = sock.accept()
            
            cThread = threading.Thread(target=self.handler , args=(c, a))
            cThread.daemon = True
            cThread.start()
        
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0])+ ':' + str(a[1]) , "connected")
            self.send_chain(chain)
            self.sendPeers()
            

    def handler(self, c, a):
        while True:
            data = c.recv(1024) 
            print("from port ::"+ str(a[1]) + "->>"+str(data, 'utf-8') )
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
        print("Latest_Peers->[" + str(bytes(p, "utf-8"))+ "] ")
        # updated , send the list of peers
        for connection in self.connections:
            # we send an extra byte \`x11 to identify the list of peers
            connection.send(b'\x11' + bytes(p, "utf-8"))
        
        #for connection in self.connections:
        #   connection.send(bytes("SERVER :: ALL IS WELL", "utf-8"))
    
    def send_chain(self,chain):
        # send the chain to every body
        print("sending chain")
        for connection in self.connections:
            connection.send(b'\x12' +bytes(chain,'utf-8'))

class Client:
    
    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))
    
    def __init__(self,address):
            self.chain = ""
            sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            sock.connect((address, 10000)) 
    
            iThread = threading.Thread(target=self.sendMsg, args=(sock, )) #sends args(i.e:: sock object) in form o ftuples
            iThread.daemon = True
            iThread.start()

            while True:
                data = sock.recv(1024)
                if not data:
                    break
                if data[0:1] == b'\x12':
                    print("CLIENT ::GOT THE CHAIN")
                    #SEND THIS CHAIN TO BLOCKCHAN.PY TO VALIDATE|| UPDATE
                    #this.chain = data

                if data[0:1] == b'\x11':
                    print("PEERS UPDATED ")
                    self.updatePeers(data[1:])
                else:
                    print("got this data :: "+ str(data, 'utf-8'))
                    #print(self.chain)
    
    def updatePeers(self , peerData):
        P2p.peers = str(peerData, "utf-8").split(",")[:-1]

#to access the peers by both the client and the server
class P2p:
    peers = ['127.0.0.1'] # set a default peer
    ports =['10000']
    # (sys.argv): command line argument , if:: cjeck if there are any second command line argument(i.e the client) , ex :- python chat.py 127.0.0.01
    #if (len(sys.argv)> 1):
    #    client = Client(sys.argv[1])
    #else:
    #    server = Server()

class P2pServer:
    def __init__(self,chain):
        self.chain = chain
        while True:
            try:
                print("trying to connect...\n-------------------------------------")
                time.sleep(randint(1,5))    
                for peer in P2p.peers:
                    try:
                        client = Client(peer)
                    except KeyboardInterrupt:
                        sys.exit(0)  
                    except:
                        pass

                    try:
                        server = Server(self.chain)
                    except KeyboardInterrupt:
                        sys.exit(0)  
                    except:
                        print("couldn't start the server ...")
            except KeyboardInterrupt:
                sys.exit(0)

p2pServer = P2pServer("+++++++SAYING HELLO--------")
