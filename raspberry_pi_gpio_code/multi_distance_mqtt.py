from gpiozero import DistanceSensor
from time import sleep
import paho.mqtt.client as mqtt

mqtt_broker = 'mqtt-broker.icenilabs.com'
mqtt_port = 1883
sensor1 = DistanceSensor(20, 21)  # echo: 20, trig: 21
sensor2 = DistanceSensor(16, 12)  # echo: 16, trig: 12
client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)

while True:
    client.publish('rpi/distance1', sensor1.distance)
    client.publish('rpi/distance2', sensor2.distance)
    sleep(.5)
