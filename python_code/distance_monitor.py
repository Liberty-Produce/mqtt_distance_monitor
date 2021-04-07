"""
DISTANCE MONITOR

Distance monitor using HC-SR04 sonar modules connected to an Arduino and controlled via a RaspberryPi connected to the
Arduino via USB port.

Readings are sent to an mqtt broker via the RaspberryPi's ethernet connection.

Wiring diagram: 'docs and images/4x_HC-SR04_(arduino).png'

Versions:
1.0 - Initial release
"""

import sys
import time
import paho.mqtt.client as mqtt
from collections import namedtuple
from pymata4 import pymata4

# List of pins for each sonar module connected to the Arduino
Pins = namedtuple('pins', 'trigger_pin echo_pin')

# Each sonar module needs its own numbered pin group in this order: trigger, echo. The module number will be used to
# identify each module to the MQTT broker and will be added to the publish topic.
sonar_pins = {
    0: Pins(2, 8),
    1: Pins(3, 9),
    2: Pins(4, 10),
    3: Pins(5, 11),
}

# Topic to publish sonar module readings to via mqtt. Module number will be added to end of this string as a
# unique identifier.
MQTT_BROKER = 'mqtt-broker.icenilabs.com'
MQTT_TOPIC = 'arduino/distance'


def main():
    while True:
        try:
            # initialise pymata library
            board = pymata4.Pymata4()
            # initialise mqtt connection
            mqtt_client = setup_mqtt(MQTT_BROKER)
            # instantiate each sonar module
            sonars = [Sonar(board, name, pins.trigger_pin, pins.echo_pin) for name, pins in sonar_pins.items()]
            # start reading loop
            take_readings(sonars, mqtt_client, MQTT_TOPIC)
            sys.exit(0)
        except KeyError:
            time.sleep(1)
            continue
        except KeyboardInterrupt:
            sys.exit(0)


def setup_mqtt(mqtt_broker: str, mqtt_port: int = 1883, keep_alive: int = 60) -> mqtt.Client:
    """
    Sets up mqtt client connection to specified broker and return client object.

    :param mqtt_broker: MQTT broker url or ip address
    :param mqtt_port: MQTT broker port
    :param keep_alive: Maximum period in seconds between communications with the broker.
    :return: MQTT client connection object
    """
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, keep_alive)
    return client


def take_readings(modules: list, mqtt_client: mqtt.Client, topic: str,
                  sleep_duration: float = 0.5):
    """
    Loops through each sonar module reading and publishes to MQTT broker on the specified topic

    :param modules: List of sonar module instances
    :param mqtt_client: MQTT client connection object
    :param topic: Topic to publish readings to via MQTT. Module number will be added to the end to give each module a
                  unique topic.
    :param sleep_duration: Time in seconds between read cycles.
    """
    while True:
        try:
            [mqtt_client.publish(f'{topic}{sonar.sonar_name}', f'{sonar.reading}') for sonar in modules]
            time.sleep(sleep_duration)
        except (KeyboardInterrupt, RuntimeError):
            # shutdown all board connections prior to quitting programme
            [sonar.close() for sonar in modules]
            break


class Sonar:
    """
    Sets up firmata connection to a sonar module via Arduino connected via using specified pins.

    :param pymata_board: Pymata connection object
    :param sonar_name: Unique identifier for sonar module.
    :param trigger_pin: Arduino pin number connected to sonar module trig pin
    :param echo_pin: Arduino pin number connected to sonar module echo pin
    """

    # _callback() data return indices
    PIN_TYPE = 0
    TRIGGER_PIN = 1
    DISTANCE_CM = 2
    TIMESTAMP = 3

    def __init__(self, pymata_board: pymata4.Pymata4, sonar_name, trigger_pin: int, echo_pin: int):
        self.board = pymata_board
        self.sonar_name = sonar_name
        self.trig = trigger_pin
        self.echo = echo_pin
        # placeholder for data set by _callback()
        self.data = [0, 0, 0, 0]
        # initialise specified pins on Arduino
        self._set_board()

    def _set_board(self) -> None:
        """
        Sets up specified pins on connected Arduino to work with sonar module
        """
        try:
            self.board.set_pin_mode_sonar(self.trig, self.echo, self._callback)
        except Exception:
            print(f'Problem setting up {self.sonar_name}')
        print(f'Set up {self.sonar_name} successfully')

    def _callback(self, data: list):
        """
        The callback function to display the change in distance returned by sonar module readings. Will be called by the
        Pymata library when a reading is requested.
        :param data: [pin_type=12, trigger pin number, distance, timestamp]
        """
        self.data = data

    @property
    def reading(self, index: str = 'cm') -> int:
        """
        Returns sonar module reading in cm

        :param index: _callback() data index to return
        :return: Sonar module reading in cm
        """
        if index == 'cm':
            index = Sonar.DISTANCE_CM
        self.board.sonar_read(self.trig)
        return self.data[index]

    def close(self) -> bool:
        self.board.shutdown()
        print(f'Shut down {self.sonar_name} successfully')
        return True


if __name__ == '__main__':
    main()
