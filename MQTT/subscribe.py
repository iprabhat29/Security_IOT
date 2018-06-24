import paho.mqtt.client as mqtt:wq
#from paho import *
broker_address = "localhost"
broker_port = 1883
import sys

USER_HOME="/user/iprabhat/TW_Project_python/MQTT/"
print "Creating new subscriber\n"

station_name = sys.argv[1]
client = mqtt.Client(station_name)



def on_message(client,userdata,message):
	print("message received ",str(message.payload.decode("utf-8")))
	with open("station","w") as f:
		f.write(str(message.payload.decode("utf-8")))
	f.close()

password = "Prabhat"

key = hashlib.sha256(password).digest()

print key

decryptor(key,'enc_file','outfile')

#mqtt.username_pw_set(username=station_name,password=station_name)

client.connect(broker_address,broker_port)

client.loop_start()
print ("New subscriber ",station_name," Connected!!\n")

print "Subscribing the new station\n"

station_dir = USER_HOME + station_name + ".txt"
print station_dir
client.subscribe("/user/iprabhat/TW_Project_python/substation1.txt",0)

