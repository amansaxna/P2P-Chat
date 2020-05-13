import socket
# server won't be able to work if multiple connections try to  access simultanesously :: therefore we create threads 
import threading
import sys 

class Server:
    #create a socket object
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 

    #all the connetions are stored winthin the array
    connections = []

    def __init__(self):
        #bind the socket object to an address + port
        self.sock.bind(('0.0.0.0', 10000))

        #open socket , listen(n) :: n = no of connection sto be allowed
        #though  never works with me it accepts more!!:>
        self.sock.listen(10)

    def handler(self, c, a):
        #global connections
        while True:
            data = c.recv(1024) 
            # now to send the data back to the clients
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0])+ '+' + str(a[1]) + "dis-connected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        #listen till true 
        while True :
            # c:: the connection , a :: client address 
            c , a = self.sock.accept()
            
            # after accepting the connection create a thread to handle that connection , pass the function that will handel the thread
            cThread = threading.Thread(target=self.handler , args=(c, a))
            # problem :if you close the server and if any thread is still running the os will not allow you to close
            #soclution
            cThread.daemon = True
            cThread.start()

            # do I need to explainn this!, Seriously!!
            self.connections.append(c)
            print(str(a[0])+ '+' + str(a[1]) + "connected")

class Client:
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 
    
    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))
    
    def __init__(self,address):
            self.sock.connect((address, 10000)) 
            # add.. = sys.argv[1]

            iThread = threading.Thread(target=self.sendMsg)
            iThread.daemon = True
            iThread.start()

            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(str(data, 'utf-8'))

# (sys.argv): command line argument , if:: cjeck if there are any second command line argument(i.e the client) , ex :- python chat.py 127.0.0.01
if (len(sys.argv)> 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()