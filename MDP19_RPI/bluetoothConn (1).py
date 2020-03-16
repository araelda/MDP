from bluetooth import *

class bluetoothConnection():

    def __init__(self):
        self.server_sock = None
        self.client_sock = None
        self.client_info = None
        self.port = None
        self.connectedStatus= False

    def startConn(self):
        while True:
            try:
                btport = 3
                #create the server socket
                self.server_sock = BluetoothSocket(RFCOMM)
                #server listens to any port
                self.server_sock.bind(("", btport))
                #listen to 1 connection at a time
                self.server_sock.listen(1)
                self.port = self.server_sock.getsockname()[1]
                uuid = "00001101-0000-1000-8000-00805F9B34FB"

                #advertise bluetooth service
                advertise_service( self.server_sock, "mdpgrp19",
                                service_id = uuid,
                                service_classes = [ uuid, SERIAL_PORT_CLASS ],
                                profiles = [ SERIAL_PORT_PROFILE ],
                                protocols = [ OBEX_UUID]
                                )

                print("[Bluetooth]Waiting for connection on RFCOMM channel %d" % self.port)
                #server accepts connection request from the client
                #client_sock is the socket used for communication with the client
                self.client_sock, self.client_info = self.server_sock.accept()
                print("[Bluetooth]Accepted connection from: ", self.client_info)
                self.connectedStatus = True
                retry = False

            except Exception as e:
                retry = True
                print("BT connection error: %s" % str(e))
                if (not retry):
                    break
                print("Retrying bluetooth connection")

    def closeConn(self):
        if self.server_sock:
            self.server_sock.close()
            print("Closing bluetooth socket on server")
        if self.client_sock:
            self.client_sock.close()
            print("Closing bluetooth socket on client")

        self.connectedStatus = False

    def read(self):
        try:
            if self.connectedStatus:
            #receive data through the server socket and assigned it to message
                message = self.client_sock.recv(1024)
                message = message.decode()
                return message
        except Exception as e:
            print("[Read from bt error]: %s" % str(e))

    def write(self, message):
        try:
            #if not connected
            if (not self.connectedStatus):
                print("Bluetooth is not connected. Transmission failed.")
            #sending the message over through the client socket
            self.client_sock.send(message)
            #print("[bluetooth]: message sent!")
        except Exception as e:
            print("[Write to bt error]: %s " %str(e))
        

#for testing
#if __name__ == "__main__":
    #test = bluetoothConnection()
    #test.startConn()

    #stay_alive = True
    #while stay_alive:
        #message = test.read()
        #print("data received from phone: %s" % message)
        #test.write("yooooo")
        #if test.read() == "exit":
            #stay_alive = False
        #else:
            #continue
    #print("Closing socket")
    #test.closeConn()
