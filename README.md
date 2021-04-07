# Multi-module distance monitor utilising HC-SR04 sonar modules, Arduino, RaspberryPi, and MQTT protocol.

## What does this do?

This project allows remote monitoring of one or more HC-SR04 sonar modules.

The modules plug into an Arduino, the Arduino is controlled by a Raspberry Pi, and the Raspberry Pi sends the data to a
NodeRed dashboard via the MQTT protocol.

## What should I know before starting this project?

- How to [set up a Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
- How to [wire up Arduino pins and uploading code via the IDE](https://www.arduino.cc/en/Tutorial/Foundations).
- How to install [Python3](https://www.python.org) and run a script.
- How to install [Node-RED](https://nodered.org/docs/getting-started)
  and [import a flow](https://nodered.org/docs/user-guide/editor/workspace/import-export)
- Basic familiarity of the [Firmata controller protocol](https://github.com/firmata/protocol).
- Basic familiarity of the [MQTT messaging protocol](https://mqtt.org).

## What hardware is needed?

This project as it's currently configured requires the following:

- [Raspberry Pi](https://www.raspberrypi.org/products) (3B or better)
- [Arduino](https://www.arduino.cc/en/main/products) ([MEGA2560](https://store.arduino.cc/arduino-mega-2560-rev3) used
  but any modern board will probably work)
- One or more [HC-SR04 sonar modules](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors) (project uses 4)

The HC-SR04 modules are wired to the Arduino as follows. You may use whichever pins on the Arduino you like but make
sure you update the script as required.

![diagram](docs_images/4x_HC-SR04_(arduino).png)

## What code is needed?

This project uses the following software / libraries:

### Arduino

- [FirmataExpress](https://www.arduino.cc/reference/en/libraries/firmataexpress/) - Accepts control commands via USB

### Raspberry Pi
- [Python3](https://www.python.org) - Runs the script
- [pymata4](https://pypi.org/project/pymata4/) - Sends control commands to the Arduino via USB
- [Eclipse Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/) - Sends readings via MQTT

### Raspberry Pi or network connected PC

- [Mosquitto MQTT Broker](https://mosquitto.org/) - Receives readings sent via MQTT and allow other devices to subscribe
  to those readings
- [Node-RED](https://nodered.org/) - Displays readings received via MQTT on a dashboard
