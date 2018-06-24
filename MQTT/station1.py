########################################
#Written By:Prabhat Bhatt
#Topic:IOT Protocol for TW Project
########################################
import paho.mqtt.client as mqtt #import the client1
import time
import sys
import hashlib
from encryptor import *
import os
from RSA_crypto import * 
broker_address="iot.eclipse.org"
#broker_address="172.30.192.171"
keygenfile()
####################################################################
from random import randint
r = randint(0, 99999)

passkey = str(r)
encfile(passkey,"0")
key1 = hashlib.sha256(passkey).digest()

r = randint(0,99999)
passkey = str(r)
encfile(passkey,"5")
key2 = hashlib.sha256(passkey).digest()

r = randint(0,99999)
passkey = str(r)
encfile(passkey,"6")
key3 = hashlib.sha256(passkey).digest()

r = randint(0,99)
p = str(r)
encfile(p,"8")
#####################################################################
#####################On_message_received do the following############
####################################################################
def on_message(client, userdata, message):	
	decrypt_msg1 = decfile("1")
	to_hash1 = hashlib.sha256(decrypt_msg1).digest()
	decrypt_msg2 = decfile("2")
	to_hash2 = hashlib.sha256(decrypt_msg2).digest()
	decrypt_msg3 = decfile("9")
	to_hash3 = hashlib.sha256(decrypt_msg3).digest()
	if message.payload == to_hash1:
		print "MESSAGE 2 from SUBSTATION1 to SERVER-->READY STATION\n"
		ret = client.publish("Mainserver",key2)
	elif message.payload == to_hash2:
		print "********DONE MESSAGE RECEIVED FROM PUBLISHER DECRYPTING FILE \n"
		print "********DECRYPTING FILE\n"
		while True:
			try:
				decryptor(key1,'Station1_sub','pubfile_dec')
				break
			except ValueError:
				print "DECRYPTING AGAIN!!!\n"
				continue	
		outfile = open('pubfile_dec','a')
		outfile.write("Parameter Applied JOB1 completed")
		outfile.close()
		print "MESSAGE FROM STATION1 to MAINSERVER-->CHECK JOB\n"
		r = randint(0,99)
		p = str(r)
		encfile(p,"8")
		key4 = hashlib.sha256(p).digest()
		ret = client.publish("Mainserver",key4)
	elif message.payload == to_hash3:
		print "********PASSED SECURITY PARAMETER JOB COMPLETED\n"
		print "MESSAGE4 from STATION1 to STATION2---->STATION1 DONE\n"
		ret = client.publish("Station2.txt",key3)
		print "********STATION1 WILL WAIT FOR 20 sec MORE BEFORE DISCONNECTIONG\n"
	else:
		with open("Station1_sub" , "a") as f:
			f.write(message.payload)
			f.close()	
######################################################################
######################################################################
###################STATION CREATION###################################
print("********CREATING NEW INSTANCE\n")
client = mqtt.Client("Station1") #create new instance
client.on_message=on_message #attach function to callback
######################################################################
######################################################################
###########################CONNECTING TO BROKER#######################
print("********CONNECTING TO BROKER\n")
client.connect(broker_address) #connect to broker
######################################################################
################################CLIENT STARTS HERE####################
client.loop_start() #start the loop
client.subscribe("Station1.txt")
#####################################################
time.sleep(20)
print "********STATION1 SIGNING OUT\n"
cmd = "ps|grep 'station1'|awk '{print $1}'>list"
os.system(cmd)
outfile = open('list','r')
out = outfile.readlines()
outfile.close()
for l in out:
	cmd = "kill " + str(l)
	os.system(cmd) 
client.loop_stop()
#client.loop_forever()
