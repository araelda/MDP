
import threading
import Queue
import time
import cv2

from arduino import *
from bluetoothConn import *
from pcConn import *
from imageReg import *
from picamera import PiCamera
from picamera.array import PiRGBArray

delay = 0.2

class Main(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.debug = True
        #initialize threads with the respective classes
        self.arduino = ArduinoConnection()
        self.bluetooth = bluetoothConnection()
        self.pc = pcConnection()
        self.camera1 = imagereg()

	#need to put from picamera import PiCamera first
	#pi camera initialization
	self.camera = PiCamera()
        self.camera.resolution = (544,240)
	#self.camera.resolution = (100, 100)
	self.camera.framerate = 50
	self.rawCapture = PiRGBArray(self.camera, size=(544, 240))
	self.image = 0 #counter to save the image
##	##### need to initialize the image processing thread to constantly ping for any incoming files saved in the folder"

        #start connections
        pc_start_thread = threading.Thread(target=self.pc.init_setupConn, name = "pc_start_thread")
        bt_start_thread = threading.Thread(target=self.bluetooth.startConn, name = "bt_start_thread")
        arduino_start_thread = threading.Thread(target=self.arduino.connect, name = "arduino_start_thread")

        pc_start_thread.daemon = True
        bt_start_thread.daemon = True
        arduino_start_thread.daemon = True

        pc_start_thread.start()
        bt_start_thread.start()
        arduino_start_thread.start()
        time.sleep(1)

    def read_from_pc(self):
        while True:
            pc_message = self.pc.readfromPC()
            if (pc_message is not None):
                    pc_message = pc_message.split('\n')
		    for msg in pc_message:
			#print("Sending to process msg: %s" % msg)
			self.process_msg(msg)
            #time.sleep(delay)

    def process_msg(self, pc_message):
	#INSTR R
	if pc_message[:2] == "IN":
	    if (pc_message[-1] != "M"):
            	self.write_to_arduino(pc_message[-1])
	    	print("Add to arduino queue: %s" % pc_message[-1])
	    	#sending to bt
	    	pc_message = "A" + pc_message[-1]
            	pc_message = "{\"status\":\"" + pc_message + "\"}"
            	self.write_to_bt(pc_message)
	    	time.sleep(delay)
	#sending json to bt
	elif "INSTR" in pc_message:
            self.write_to_arduino(pc_message[-1])
	    #sending the json file
	    self.write_to_bt(pc_message[:-6])
	    self.write_to_bt("A" + pc_message[-1])
	elif (len(pc_message) in range (40, 50)):
            self.take_picture(pc_message, self.debug)
        elif "END" in pc_message:
            #self.write_to_bt(pc_message[:-3])
            #self.write_to_bt(pc_message[-3:])
            #results = self.camera1.process_img("", "END")
            #print("Results: %s" % results)
            #self.write_to_bt("END")
            results = self.camera1.process_img("", "END")
            print("Results: %s" % results)
            self.write_to_bt(results)
	elif "FP_END" in pc_message:
	    self.write_to_bt("FP_END")
	else:
            self.write_to_bt(pc_message)
	
     		    
    def write_to_pc(self, messagetoPC):
        if messagetoPC is not None:
            self.pc.writetoPC(messagetoPC)
            print("Wrote to pc: %s" % messagetoPC)

    #android to pc for waypoint and coordinates and directions
    def read_from_bt(self):
        while True:
            bt_message = self.bluetooth.read()
            if (bt_message is not None):
                    print("Bluetooth read: %s" % bt_message)
                    self.write_to_pc(bt_message + '\n')
	    #time.sleep(delay)

    def write_to_bt(self, messagetoBT):
        if messagetoBT is not None:
            self.bluetooth.write(messagetoBT)
            print("Wrote to bluetooth: %s" % messagetoBT)

    def write_to_arduino(self, messagetoARD):
        if messagetoARD is not None:
            if (messagetoARD[:1] != "{"):
                self.arduino.sendMsg(messagetoARD)
                #time.sleep(delay)
    
    #sends to pc the sensor values etc
    def read_from_arduino(self):
        while True:
            ard_message = self.arduino.readMsg()
            if (ard_message is not None):
                print("Arduino read: %s" % ard_message)
		#sending sensor values
                if ("SDATA" in ard_message):
                    #ard_message = ard_message.replace('I', 'Sensor')
                    self.write_to_pc(ard_message)
    
                
            #time.sleep(delay)

    def take_picture(self, imgMsg, debug):
        print("in picture taking function")
	print("json string: %s" % imgMsg)
        self.image += 1
        self.camera.capture(self.rawCapture, format="rgb", use_video_port=True)
        img = self.rawCapture.array
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if (debug):
            cv2.imwrite("test/" + str(self.image) + "raw.jpg", img)
        results = self.camera1.process_img(img, imgMsg)
        print("Results: %s" % results)     
        self.write_to_bt(results)


	self.rawCapture.truncate(0) #clear the stream
        #send the json string to android
##	self.write_to_bt(results)

    def initialize_threads(self):
        #initialize the threads
        pc_read_thread = threading.Thread(target=self.read_from_pc, name = "pc_read_thread")
        bt_read_thread = threading.Thread(target=self.read_from_bt, name = "bt_read_thread")
        arduino_read_thread = threading.Thread(target=self.read_from_arduino, name = "arduino_read_thread")

        #set the threads to daemon
        pc_read_thread.daemon = True
        bt_read_thread.daemon = True
        arduino_read_thread.daemon = True

        #start the threads
        pc_read_thread.start()
        bt_read_thread.start()
        arduino_read_thread.start()

        print("All threads started")

    def keep_alive(self):
        while True:
            time.sleep(5)

    def close_sockets(self):
        self.bluetooth.closeConn()
        self.pc.closeConn()
        self.arduino.disconnect()

if __name__ == "__main__":
        mainThread = Main()
        mainThread.initialize_threads()
        mainThread.keep_alive()
        mainThread.close_sockets()
                    

