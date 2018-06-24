########################################
#Written By:Prabhat Bhatt
#Topic:IOT Protocol for TW Project
########################################



import paho.mqtt.client as mqtt #import the client1
import time
import sys
import hashlib
from encryptor import *
import thread

#broker_address="192.168.1.184"

broker_address="iot.eclipse.org"

passkey = "Prabhat"
key1 = hashlib.sha256(passkey).digest()





#####################On_message_received do the following################
def on_message(client, userdata, message):
	print "Payload Received\n"

#	print(message.payload)
#	print(str(message.payload.decode("utf-8")))
	
	with open("Station3_sub" , "a") as f:
#		print "writing the current messsage\n"
#		print "Decrypting Message......\n"
		f.write(message.payload)   #wiriting payload which will be encrypted
		f.close()	

#########################################################################



#########client creation which is substation1#################

print("creating new instance")

client = mqtt.Client("Station3") #create new instance

client.on_message=on_message #attach function to callback

##############################################################


###########Connecting client to broker#######################

print("connecting to broker")

client.connect(broker_address) #connect to broker

############################################################


###############Client start here####################

client.loop_start() #start the loop

print("Subscribing to topic","Station3.txt")  

#subscribing to a topic station1 will subscribe to station1.txt

client.subscribe("Station3.txt")

#####################################################

time.sleep(20) # wait
###########Finally Decrypting File to check whether correct file was received########

decryptor(key1,'Station3_sub','pubfile_dec3')
time.sleep(5)
client.loop_stop()
