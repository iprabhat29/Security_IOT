########################################
#Written By:Prabhat Bhatt
#Topic:IOT Protocol for TW Project
########################################
import paho.mqtt.client as mqtt #import the client1
import time
import sys
import hashlib
from random import randint
from encryptor import *
import thread
counter = 0
from RSA_crypto import *
broker_address="172.30.192.171"
#broker_address="iot.eclipse.org"
##########################################################
#########################################################
passkey = decfile("0")
key1 = hashlib.sha256(passkey).digest()

r =randint(0,99999) 
passkey = str(r)
encfile(passkey,"7")
key2 = hashlib.sha256(passkey).digest()

r = randint(0,99)
passkey = str(r)
encfile(passkey,"10")

r=randint(0,99999)
p = str(r)
encfile(p,"10")
#####################On_message_received do the following################
#########################################################################
def on_message(client, userdata, message):
	dec_passkey1 = decfile("6")
	dec_hashkey1 = hashlib.sha256(dec_passkey1).digest()
	dec_passkey2 = decfile("3")
	dec_hashkey2 = hashlib.sha256(dec_passkey2).digest()
	dec_passkey3 = decfile("11")
	dec_hashkey3 = hashlib.sha256(dec_passkey3).digest()
	dec_passkey4 = decfile("12")
	dec_hashkey4 = hashlib.sha256(dec_passkey4).digest()
	if message.payload == dec_hashkey1:
		print "MESSAGE* from SUBSTATION2 to SERVER-->READY STATION\n"
		ret = client.publish("Mainserver",key2)
	elif message.payload == dec_hashkey4:
		print "MESSAGE* from SUBSTATION2 to SERVER-->READY STATION\n"
		ret = client.publish("Mainserver",key2)
	elif message.payload == dec_hashkey2:
		print "******DONE MESSAGE RECEIVED FROM PUBLISHER DECRYPTING FILE \n"
		print "********DECRYPTING FILE\n"
		while True:
			try:
				decryptor(key1,'Station2_sub','pubfile_dec2')
				break
			except ValueError:
				print "DECRYPTING AGAIN"
				continue
		outfile = open('pubfile_dec2','a')
		outfile.write("Parameter Applied JOB2 completed")
		outfile.close()
		print "MESSAGE* FROM STATION2 to MAINSERVER-->CHECK JOB\n"
		r = randint(0,99)
		p = str(r)
		encfile(p,"10")
		key3 = hashlib.sha256(p).digest()
		ret = client.publish("Mainserver",key3)
		#print "********MESSAGE* CLIENT WILL WAIT FOR 20 sec MORE BEFORE DISCONNECTIONG\n"
	elif message.payload == dec_hashkey3:
		print "********PASSED SECURITY PARAMETER JOB COMPLETED\n"
		print "MESSAGE* from STATION2 to STATION3---->STATION2 DONE\n"
		ret = client.publish("Station3.txt",key2)
		print "********STATION1 WILL WAIT FOR 20 sec MORE BEFORE DISCONNECTIONG\n"
	
		
	else:
		with open("Station2_sub" , "w") as f:
			f.write(message.payload)   #wiriting payload which will be encrypted
			f.close()	
##############################################################
#########client creation which is substation1#################
client = mqtt.Client("Station2") #create new instance
client.on_message=on_message #attach function to callback
#############################################################
###########Connecting client to broker#######################
print("********CONNECTING TO BROKER\n")
client.connect(broker_address) #connect to broker
############################################################
###############Client start here############################
client.loop_start() #start the loop
print("********SUBSCRIBING TO TOPIC Station2.txt\n")  
client.subscribe("Station2.txt")
###########################################################
###########################################################
time.sleep(20)
print "********STATION2 SIGNING OUT"
cmd = "ps|grep 'station2.py'|awk '{print $1}'>list"
os.system(cmd)
outfile = open('list','r')
out = outfile.readlines()
outfile.close()
for l in out:
	cmd = "kill " + str(l)
	os.system(cmd) 
client.loop_stop()
