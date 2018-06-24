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

############Generating KEY for encryption##########
passkey = "Prabhat"
key1 = hashlib.sha256(passkey).digest()
print key1


####################################################

#####################On_message_received do the following################
def on_message(client, userdata, message):
	print "Payload Received\n"

#	print(message.payload)
#	print(str(message.payload.decode("utf-8")))
	
	with open("Station1_sub.txt" , "a") as f:
		print "writing the current messsage\n"
		print "Decrypting Message......\n"
		f.write(message.payload)   #wiriting payload which will be encrypted
		f.close()	

#########################################################################




#############Publisher Thread###########################

def publisher_thread(threadname,key):
	pubfile = "station1.txt"
	print "Thread Name\n"
	print "File that need to be encrypted" , pubfile	
	
#########################################################


#broker_address="192.168.1.184"
broker_address="iot.eclipse.org"


#########client creation which is substation1#################

print("creating new instance")

client = mqtt.Client("Station1") #create new instance

client.on_message=on_message #attach function to callback

##############################################################


###########Connecting client to broker#######################

print("connecting to broker")

client.connect(broker_address) #connect to broker

############################################################


###############Client start here####################

client.loop_start() #start the loop

print("Subscribing to topic","Station1.txt")  

#subscribing to a topic station1 will subscribe to station1.txt

client.subscribe("Station1.txt")

#####################################################


print("Publishing Encrypted message to topic","Station1.txt")

#########ENCRYPTION################################

print "Encryption Began\n"

encryptor(key1,"station1.txt",'pubfile_enc')

##################################################


################Publishing Encrypted file below########

file = open('pubfile_enc',"rb")

for line in file:
	ret = client.publish("Station1.txt",line)
file.close()

#######################################################

try:
	thread.start_new_thread( publisher_thread, ("Thread 1", key1,))
except:
	print "Unable to spawn a thread!!"

time.sleep(4) # wait

###########Finally Decrypting File to check whether correct file was received########

decryptor(key1,'pubfile_enc','pubfile_dec')

#####################################################################################
client.loop_stop() #stop the loop
