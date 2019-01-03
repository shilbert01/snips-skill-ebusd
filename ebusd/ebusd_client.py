import time
import paho.mqtt.client as paho

class SnipsEbusd(object):
	def __init__(self, ipaddress):
	    broker = ipaddress
	    self.client = paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
	    
	    ##print("connecting to broker ",broker)
	    self.client.connect(broker)#connect

	def on_message(self.client, userdata, message):
	    time.sleep(1)
	    print("received message =",str(message.payload.decode("utf-8")))
	    return str(message.payload.decode("utf-8"))

	def setHwcQuickVetoTemp(self,temp):
	    self.client.publish("ebusd/430/HwcQuickVetoTemp/set",temp)#publish
	    time.sleep(2) # sleep 2 seconds and then subscribe to mqtt message 'HwcQuickVetoTemp' - this results in ebusd/430/HwcQuickVetoTemp {"temp1": {"value": 44.0}}
	    result = self.client.subsribe("ebusd/430/HwcQuickVetoTemp")
	    #self.client.disconnect() #disconnect
	    return True

	def getHwcQuickVetoTemp(self):
	    HwcQuickVetoTemp = self.client.publish("ebusd/430/HwcQuickVetoTemp/get")#publish
	    #self.client.disconnect() #disconnect
	    return HwcQuickVetoTemp

	def getHeatingCurve(self):
	    ######Bind function to callback
	    self.client.on_message=on_message
	    self.client.loop_start() #start loop to process received messages
	    print("subscribing ")
	    self.client.subscribe("sonoff_ebus/mc/HeatingCurve/curve")#subscribe
	    time.sleep(2)
	    print("publishing ")
	    self.client.publish("sonoff_ebus/mc/HeatingCurve/curve/get","HeatingCurve")#publish
	    time.sleep(4)
	    print self.client.on_message
	    #client.disconnect() #disconnect
	    client.loop_stop() #stop loop

	def setHeatingCurve(self,curve):
	    self.client.publish("sonoff_ebus/mc/HeatingCurve/curve/set",curve)#publish
	    time.sleep(2) # sleep 2 seconds and then subsrive to mqtt message 'HwcQuickVetoTemp' - this results in ebusd/430/HwcQuickVetoTemp {"temp1": {"value": 44.0}}
	    result = self.client.subsribe("sonoff_ebus/mc/HeatingCurve/curve/#")
	    #self.client.disconnect() #disconnect
	    return True