#########################################
#Written By:Prabhat Bhatt
#Topic:IOT Protocol for TW Project
########################################
import paho.mqtt.client as mqtt #import the client
import time
import sys
####Generating KEY for encryption##########

#####################################################
#broker_address="172.30.192.171"
broker_address = "broker.hivemq.com"
#broker_address="iot.eclipse.org"
########################################################
def on_message(client, userdata, message):
	dec_passkey1 = decfile("5")
	dec_key_hash = hashlib.sha256(dec_passkey1).digest()
	dec_passkey2 = decfile("7")
	dec_key_hash2 = hashlib.sha256(dec_passkey2).digest()	
	dec_passkey3 = decfile("8")
	dec_key_hash3 = hashlib.sha256(dec_passkey3).digest()
	dec_passkey4 = decfile("10")
	dec_key_hash4 = hashlib.sha256(dec_passkey4).digest()
	if message.payload == dec_key_hash:
		file = open('pubfile_enc',"rb")
		for line in file:
			ret = client.publish("Station1.txt",line)
		file.close()
		print "MESSAGE* From SERVER to STATION1--->DONE STATION1\n"
		ret = client.publish("Station1.txt",key_hash1)
	elif message.payload  == dec_key_hash2:
		file = open('pubfile_enc2',"rb")
		for line in file:
			ret = client.publish("Station2.txt",line)
		print "MESSAGE* From SERVER to STATION2--->DONE STATION2\n"
		ret = client.publish("Station2.txt",key_hash2)
		file.close()
	elif message.payload == dec_key_hash3:
		print "********PARAMETER RECEIVED FROM STATION1 LETS CHECK\n"
		if int(dec_passkey3) > 90:
			print "MESSAGE* FROM MAINSERVER TO STATION1-->WELL DONE!--->",dec_passkey3
			ret = client.publish("Station1.txt",key_hash4)
		else:
			print "MESSAGE* FROM MAINSERVER TO STATION1-->DO THE JOB AGAIN!!"
			cmd = "rm Station1_sub"
			os.system(cmd)
			cmd = "rm pubfile_dec"
			os.system(cmd)
			ret = client.publish("Station1.txt",key_hash)
	elif message.payload == dec_key_hash4:
		print "********PARAMETER RECEIVED FROM STATION2 LETS CHECK\n"
		if int(dec_passkey4) > 90:
			print "MESSAGE* FROM MAINSERVER TO STATION2-->WELL DONE!--->",dec_passkey4
			ret = client.publish("Station2.txt",key_hash5)
		else:
			print "MESSAGE* FROM MAINSERVER TO STATION2-->DO THE JOB AGAIN!!"
			cmd = "rm Station2_sub"
			os.system(cmd)
			cmd = "rm pubfile_dec2"
			os.system(cmd)
			ret = client.publish("Station2.txt",key_hash6)
		
	elif message.payload == "READY STATION3":
		#print "Creating file for Station3"
		file = open('pubfile_enc3',"rb")
		for line in file:
			ret = client.publish("Station3.txt",line)
		print "MESSAGE3 From SERVER to STATION3--->DONE STATION3\n"
		ret = client.publish("Station3.txt","DONE STATION3")
		file.close()
	

#############################################################			
#########client creation which is substation1#################
#############################################################
print("********CREATING MAINSERVER\n")
client = mqtt.Client("Server") #create new instance
client.on_message=on_message #attach function to callback
##############################################################
###########Connecting client to broker#######################
############################################################
print("********CONNECTING TO BROKER\n")
client.connect(broker_address) #connect to broker
############################################################
###############Client start here##########################
client.loop_start() #start the loop
client.subscribe("Mainserver")
###########################################################
#################ENCRYPTION################################
print "********ENCRYPTION BEGINS\n"
#encryptor(key1,"station1.txt",'pubfile_enc')
#encryptor(key1,"station2.txt",'pubfile_enc2')
#encryptor(key1,"station3.txt",'pubfile_enc3')
############################################################
######MESSAGE1 From SERVER TO SUBSTATION###################
print "MESSAGE* from SERVER to SUBSTATION--> ACK STATION\n"
#ret = client.publish("Station1.txt",key_hash)
#######################################################
time.sleep(40) # wait
###########Finally Decrypting File to check whether correct file was received########
#decryptor(key1,'pubfile_enc','pubfile_dec')
#####################################################################################
print "********MAINSERVER SIGNING OUT\n"
cmd = "ps|grep 'publisher'|awk '{print $1}'>list"
os.system(cmd)
outfile = open('list','r')
out = outfile.readlines()
outfile.close()
for l in out:
	cmd = "kill " + str(l)
	os.system(cmd) 
client.loop_stop()
client.loop_stop() #stop the loop
