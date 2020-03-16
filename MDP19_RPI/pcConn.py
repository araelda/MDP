import socket
import time

class pcConnection():

    #constructor method
    def __init__(self):
        #PLS CHANGE TO 192.168.19.19 IN ACTUAL RPI
        self.host = "192.168.19.19"
        self.port = 8888
        self.socket = None
        self.client = None
        self.address = None
        self.connected = False

    def init_setupConn(self):
        while True:
            retry = False
            try:
                #create the socket
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Socket created")
                #for reusing the address
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                self.socket.bind((self.host, self.port)) #setting up the connection
                self.socket.listen(1) #allow one connection at a time
                print("Waiting for pc connection....")
                self.client, self.address = self.socket.accept()
                print("Connected to: ", self.address)
                self.connected = True
                retry = False
            except Exception as e:
                print("[PC init conn error]: %s" % str(e))
                retry = True
            if (not retry):
                break
            print("broke")
            time.sleep(1)
                           
    def closeConn(self):
        if self.client:
            self.client.close() #closing the client socket
        if self.socket:
            self.socket.close()

    def readfromPC(self):
        try:
            if self.connected:
                pcData = self.client.recv(2048) #receive data from the client, 1024 bytes max
                return pcData
            return None
        except Exception as e:
            print("[Reading from PC error]: %s" % str(e))
            self.closeConn() #close the connection
            self.init_setupConn() #restart the connection

    def writetoPC(self, message):
        try:
            if self.connected:
                self.client.sendto(message, self.address) #send the data to the address
                print("message have been sent over to pc!")
        except Exception as e:
            print("[Writing to PC Error]: %s" % str(e))
            self.closeConn() #close the connection
            self.init_setupConn() #restart the connection

if __name__ == "__main__":
    pc = pcConnection()
    #call the connection function
    pc.init_setupConn()
    if pc.connected:
        print("data received: %s" % pc.readfromPC())
        pc.writetoPC('A\n')
    
