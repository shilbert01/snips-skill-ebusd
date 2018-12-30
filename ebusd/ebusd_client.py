import time
import paho.mqtt.client as paho

class SnipsEbusd(object):
	def __init__(self, ipaddress):
	    broker = ipaddress
	    self.client = paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
	    ##print("connecting to broker ",broker)
	    self.client.connect(broker)#connect

	def setHwcQuickVetoTemp(self,temp):
	    self.client.publish("sonoff_ebus/430/HwcQuickVetoTemp/set",temp)#publish
	    #self.client.disconnect() #disconnect
	    return True

	def getHwcQuickVetoTemp(self):
	    HwcQuickVetoTemp = self.client.publish("sonoff_ebus/430/HwcQuickVetoTemp/get")#publish
	    #self.client.disconnect() #disconnect
	    return HwcQuickVetoTemp

