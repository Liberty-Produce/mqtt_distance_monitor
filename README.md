# Multi-module distance monitor utilising HC-SR04 sonar modules, Arduino, RaspberryPi, and MQTT protocol.

## What does this do?

This project allows remote monitoring of one or more HC-SR04 sonar modules.

The modules plug into an Arduino, the Arduino is controlled by a Raspberry Pi, and the Raspberry Pi sends the data to a
NodeRed dashboard via the MQTT protocol.

## What hardware is needed?

This project as it's currently configured requires the following:

- [Raspberry Pi](https://www.raspberrypi.org/products) (3B or better)
- [Arduino](https://www.arduino.cc/en/main/products) ([MEGA2560](https://store.arduino.cc/arduino-mega-2560-rev3) used
  but any modern board will probably work)
- One or more [HC-SR04 sonar modules](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors) (project uses 4)

The HC-SR04 modules are wired to the Arduino as follows. You may use whichever ports on the Arduino you like but make
sure you update the script as required.

![diagram](docs_images/4x_HC-SR04_(arduino).png)

## What code is needed?

This project uses the following libraries:

### Arduino

- [FirmataExpress](https://github.com/MrYsLab/FirmataExpress)
