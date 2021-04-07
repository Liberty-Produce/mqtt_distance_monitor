# Multi-module distance monitor utilising HC-SR04 sonar modules, Arduino, RaspberryPi, and MQTT protocol.

## What does this do?

This project allows remote monitoring of one or more HC-SR04 sonar modules.

The modules plug into an Arduino, the Arduino is controlled by a Raspberry Pi, and the Raspberry Pi sends the data to a
NodeRed dashboard via the MQTT protocol.
---

## What should I know before starting this project?

- How to [set up a Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
- How to [wire up Arduino pins and upload code via the IDE](https://www.arduino.cc/en/Tutorial/Foundations).
- How to install [Python3](https://wiki.python.org/moin/BeginnersGuide/Download) and run a script.
- How to install [Node-RED](https://nodered.org/docs/getting-started)
  and [import a flow](https://nodered.org/docs/user-guide/editor/workspace/import-export)
- Basic familiarity of the [Firmata controller protocol](https://github.com/firmata/protocol).
- Basic familiarity of the [MQTT messaging protocol](https://mqtt.org).

---

## What hardware is needed?

This project as it's currently configured requires the following:

- [Raspberry Pi](https://www.raspberrypi.org/products) (3B or better)
- [Arduino](https://www.arduino.cc/en/main/products) ([MEGA2560](https://store.arduino.cc/arduino-mega-2560-rev3) used
  but any modern board will probably work)
- One or more [HC-SR04 sonar modules](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors) (project uses 4)

---

## What code is needed?

This project uses the following software / libraries:

### Arduino

- [FirmataExpress](https://www.arduino.cc/reference/en/libraries/firmataexpress/) - Accepts control commands via USB

### Raspberry Pi

- [Python3](https://www.python.org) - Runs the script
- [pymata4](https://pypi.org/project/pymata4/) - Sends control commands to the Arduino via USB
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) - Sends readings via MQTT

### Raspberry Pi or network connected PC

- [Mosquitto MQTT Broker](https://mosquitto.org/) - Receives readings sent via MQTT and allow other devices to subscribe
  to those readings
- [Node-RED](https://nodered.org/) - Displays readings received via MQTT on a dashboard

---

## Project steps

### Step 1: Setup the Arduino pins

Wire the HC-SR04 modules to the Arduino as follows:

> red: 5v power - powers the module  
> black: ground - completes the circuit  
> green: trigger - receives read command from Arduino  
> yellow: echo - sends distance signal to Arduino

You may use whichever pins on the Arduino you like, just make sure you update the script as required.

![diagram](docs_images/4x_HC-SR04_(arduino).png)

### Step 2: Upload FirmataExpress onto the Arduino

The easiest way is to use the official Arduino IDE

1. Go to `Tools > Manage Libraries`
   to [download and install the FirmataExpress library](https://www.arduino.cc/reference/en/libraries/firmataexpress/)
1. Go to `File > Examples > FirmataExpress > FirmataExpress` to open the FirmataExpress code.
1. Upload onto the Arduino

### Step 3: Setup the Raspberry Pi

1. Set up the Pi with the latest Raspberry Pi OS
1. Update Pi and install dependencies
   ```shell
   $ sudo apt update && sudo apt -y dist-upgrade
   $ sudo apt install python3
   ```
1. Connect Raspberry Pi to the Arduino with a USB cable (any port is fine)

### Step 4: Download and install python script

Either clone or download this repo and move the distance_monitor directory containing distance_monitor.py into a
directory of your choice.  
For this example we'll be using /opt/distance_monitor. **Note you'll need to use sudo to move files into /opt.**

1. Move scrip directory to /opt:

    ```shell
    $ cd ~/distance_monitor-main  # or wherever you downloaded this repo
    $ sudo mv distance_monitor/ /opt
    ```     

1. Check files were moved correctly
    ```shell
    $ ls /opt/distance_monitor
   
   # should return:
   distance_monitor.py  requirements.txt
   ```

### Step 5: Install Python dependencies

1. Create and activate virtual environment (optional but recommended)
    ```shell
    $ cd /opt/distance_monitor
    $ python3 -m venv venv 
    $ source venv/bin/activate
    ```

1. Use pip to install dependencies listed in requirements.txt

   ```shell
   $ pip3 install -r requirements.txt
   ```

**The code can now be run via this command (if you get USB permission issues run as sudo):**

```shell
$ /opt/distance_monitor/venv/bin/python3 /opt/distance_monitor/distance_monitor.py
```

`CMD + C` will stop the programme

### Step 6: Make the script run at startup using systemd (optional)

If you're happy to run this script manually or have some other way to running it you can skip this step.  
This example assumes you'll be running the script as root, but your needs may vary.

1. Copy distance_monitor.service to the systemd directory

   ```shell
   $ cd ~/distance_monitor-main  # or wherever you downloaded this repo
   $ sudo cp raspberrypi/distance_monitor.service /etc/systemd/system/
   ```
1. Ensure Python and script paths are correct
    ```shell
    $ sudo nano /etc/systemd/system/distance_monitor.service
    ```

1. Check that ExecStart and WorkingDirectory point to the right files. Change these to match wherever you put the
   script.

   ```ini
   [Service]  
   ExecStart=/opt/distance_monitor/venv/bin/python3 /opt/distance_monitor/distance_monitor.py  
   WorkingDirectory=/opt/distance_monitor/
   ```
1. Save the file with `CMD + O` and close the editor with `CMD + X`

1. Reload the daemon to ensure systemd sees the new file
    ```shell
    $ sudo systemctl daemon-reload
    ```

1. Set the service to run at boot
    ```shell
    $ sudo systemctl enable distance_monitor
    ```

1. Start the service manually (optional)
    ```shell
   $ sudo systemctl start distance_monitor 
   ```

### Step 7: Setup MQTT broker

Head to the [mosquitto download page](https://mosquitto.org/download) and follow the instructions relevant to the OS
you'll be using.

**If you're installing both mosquitto and Node-RED on the Raspberry Pi, you can skip the next steps.**

If you're using a separate machine, you'll need to configure mosquitto to allow remote connections as by default it only
works locally.

1. Create and open a new mosquitto config file
    ```shell
    $ sudo nano /etc/mosquitto/conf.d/custom.conf
    ```
1. Add the following text to the file.
    ```text
    allow_anonymous true
    listener 1883
    ```
   Save & close with `CMD + O` and  `CMD + X`

Note this opens up the mosquitto service to **all machines connected to the network** and has no security or authentication
enabled. Steps for securing mosquitto are available but are outside the scope of this guide.

### Step 8: Setup Node-RED
