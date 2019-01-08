import time
import paho.mqtt.client as mqtt
from queue import Queue

q=Queue()

def on_log(client, userdata, level, buf):
	print("log: ",buf)

def on_disconnect(client, userdata, flags, rc=0):
	print("DisConnected flags"+"result code "+str(rc))
	client.connected_flag=False

def on_connect(client, userdata, flags, rc):
	if rc == 0:
	    client.connected_flag=True # set flag
	    print("connected OK")
	else:
	    client.bad_connection_flag=True
	    print("Bad connection Return code=", rc)

def on_message(client, userdata, message):
	client.on_message_flag=True #set flag
	print("received message =",str(message.payload.decode("utf-8")))
	file = open('/home/pi/onmessagefile.txt','w') 
	file.write(str(message.payload.decode("utf-8")))
	file.close()
	q.put(str(message.payload.decode("utf-8")))

class SnipsEbusd(object):
	def __init__(self, ipaddress):
	    self.broker_ip = ipaddress
	    mqtt.Client.connected_flag=False # create flag in class
	    mqtt.Client.bad_connection_flag=False

	def mqtt_messenger(self,subscription_topic,pub_topic,pub_msg):
	    broker=self.broker_ip
	    client = mqtt.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
	    client.on_log=on_log #client logging
	    client.on_message=on_message #bind call back function
	    client.on_connect=on_connect #bind call back function
	    client.on_disconnect=on_disconnect
	    client.loop_start() #start loop to process received messages
	    print("connecting to broker ",broker)
	    try:
		client.connect(broker)#connect
	    except:
		return "An error occured. I was not able to connect to the ebus mqtt server"
	    while not client.connected_flag and not client.bad_connection_flag: # wait in loop
	    	print(client.connected_flag)
	    	print("In wait loop")
	    	time.sleep(1)
		if client.bad_connection_flag:
		    client.loop_stop()     # Stop loop
		    return "An error occured during mqtt connection. Bad connection return code was raised"
	    print("In Main loop")
	    client.subscribe(subscription_topic)#subscribe
	    ret = client.publish(pub_topic,pub_msg,0)#publish
	    print("publish",ret)
	    time.sleep(1)
	    while not q.empty():
		results = q.get()
	    print("message payload",results)
	    client.loop_stop() #stop loop
	    client.disconnect() #disconnect
	    return results

	def getHwcQuickVetoTemp(self):
	    topic = "ebusd/430/HwcQuickVetoTemp" #publish
	    pub_topic, pub_msg = topic+"/get", "HwcQuickVetoTemp"
	    result = self.mqtt_messenger(topic,pub_topic,pub_msg)
	    return result

	def setHwcQuickVetoTemp(self,temp):
	    result = 0
	    topic = "ebusd/430/HwcQuickVetoTemp"#publish
	    pub_topic, pub_msg = topic+"/set", temp
	    while result != temp:
		result = self.mqtt_messenger(topic,pub_topic,pub_msg)
		print("result",result,"temp",temp)
	    return result

	def getHeatingCurve(self):
	    topic = "sonoff_ebus/mc/HeatingCurve/curve" #publish
	    pub_topic,pub_msg = topic+"/get","HeatingCurve"
	    result = self.mqtt_messenger(topic,pub_topic,pub_msg)
	    return result

	def setHeatingCurve(self,curve):
	    result = 0
	    topic = "sonoff_ebus/mc/HeatingCurve/curve" #publish
	    pub_topic, pub_msg = topic+"/set", curve
	    while result != curve:
		result = self.mqtt_messenger(topic,pub_topic,pub_msg)
		print("result",result,"curve",curve)
	    return result

    def getHotWaterTemp(self):
	    topic = "sonoff_ebus/ehp/hwctemp/temp" #publish
	    pub_topic,pub_msg = topic+"/get","hwctemp"
	    result = self.mqtt_messenger(topic,pub_topic,pub_msg)
	    return result
