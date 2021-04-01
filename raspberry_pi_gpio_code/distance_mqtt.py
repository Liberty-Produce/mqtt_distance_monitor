from gpiozero import DistanceSensor
from time import sleep
import paho.mqtt.client as mqtt

mqtt_broker = 'mqtt-broker.icenilabs.com'
mqtt_port = 1883
sensor = DistanceSensor(20, 21)
client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)

while True:
    client.publish('rpi/distance1', sensor.distance)
    sleep(.5)
