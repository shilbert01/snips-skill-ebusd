import time
import paho.mqtt.client as paho

class SnipsEbusd(object):
	def __init__(self, ipaddress):
	    broker = ipaddress
	    self.client = paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
	    ######Bind function to callback
	    self.client.on_message=on_message
	    #####
	    ##print("connecting to broker ",broker)
	    self.client.connect(broker)#connect
	    self.client.loop_start() #start loop to process received messages

	def setHwcQuickVetoTemp(self):
	    self.client.publish("sonoff_ebus/430/HwcQuickVetoTemp/set","52")#publish
	    time.sleep(4)
	    self.client.disconnect() #disconnect
	    self.client.loop_stop() #stop loop
	    return True

