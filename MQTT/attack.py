import paho.mqtt.client as mqtt
broker_address="10.0.0.165"
def on_message(client, userdata, msg):
   print msg.payload
client = mqtt.Client(client_id = "Station1")
#client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address)
#client.connect('iot.eclipse.org')
client.subscribe('Station1.txt')
client.loop_forever()
