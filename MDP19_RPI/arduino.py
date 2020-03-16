import serial
import threading
import time
import os

class ArduinoConnection(object):
    def __init__(self):
        self.bufFile = '/dev/ttyACM0'
        self.baudRate = 115200
        self.serConn = None

    def connect(self):
        if (os.path.exists('/dev/ttyACM0') == True):
            self.bufFile = "/dev/ttyACM0"
        elif (os.path.exists('/dev/ttyACM1') == True):
            self.bufFile = "/dev/ttyACM1"
        elif (os.path.exists('/dev/ttyACM2') == True):
            self.bufFile = "/dev/ttyACM2"
        elif (os.path.exists('/dev/ttyACM3') == True):
            self.bufFile = "/dev/ttyACM3"
        self.serConn = serial.Serial(self.bufFile,self.baudRate)
        self.serConn.flush()
        print("Connected to arduino")
    
    def readMsg(self):
        while self.serConn == None: 
            self.connect()
        try:
            data = self.serConn.readline()
            return data
        except Exception as  e:
            print("Error reading from arduino", str(e))
                
    def sendMsg(self, msg):
        while self.serConn == None: 
            self.connect()
        try:
            self.serConn.write(msg)
            print(msg , "sent")
	    self.serConn.flush()
        except Exception as e:
            print("Error writing to arduino", str(e))

    def disconnect(self):
        self.serConn.close()
        print("Arduino Disconnected")

