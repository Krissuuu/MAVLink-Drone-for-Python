# AED_Drone Python Program

## Installing
Refer to https://github.com/dronekit/dronekit-python
```
pip install dronekit
```
Refer to https://github.com/eclipse/paho.mqtt.python
```
pip install paho-mqtt
```
## Build the Ardupilot SITL
1. ***If you use Linux pls skip this step***, Install WSL (Win10 Subsystem).
2. Follow https://ardupilot.org/dev/docs/building-setup-linux.html#building-setup-linux to setup the SITL environment.
3. Follow https://github.com/ArduPilot/ardupilot/blob/master/BUILD.md to build the SITL source code. ***I use ./waf configure --board sitl***
4. ***If you use Linux pls skip this step***, Download https://sourceforge.net/projects/vcxsrv/ to visualize the Linux windows.
5. Input the command ***<sim_vehicle.py -v ArduCopter --console>*** on WSL terminal to run SITL. ***Input command <sim_vehicle.py -h> to see how to use the exist parameters***
6. Open ***Mission Planner*** or ***QGroundControl*** to control the virtual drone.
7. If you want to use ***AirSim*** virtual enviroment, start the ***Unreal Engine***, the ***setting.json*** file must to be set first, pls refer to https://ardupilot.org/dev/docs/sitl-with-airsim.html.
8. After press the ***PLAY*** buttom on ***Unreal Engine***, input the command ***<sim_vehicle.py -v ArduCopter -f airsim-copter --console>*** on WSL terminal to connect the Airsim.

## How to use

1. Run Ardupilot SITL by using this command ***sim_vehicle.py -v ArduCopter --console --custom-location=25.043014,121.536216,10,90*** on Linux terminal.

![](https://i.imgur.com/0aSJuM0.jpg)

2. Run ```__init__.py``` 

![](https://i.imgur.com/4tUAzUs.png)

## Reference
1. You can change the Ardupilot SITL IP & port from ```__init__.py```
```python=1
connection_string = '127.0.0.1:14551'
```
2. You can change the MQTT IP & port and user name & pwd from ```MQTT.py```
```python=1
self.client.username_pw_set('aiotlab', password='aiotlab208')
self.client.connect("35.201.182.150", 1883, 60)
```
3. For publishing some drone information like message, cmd_ack...., you can change the MQTT broker topic name from ```drone_msg.py```
```python=1
self.mqtt.publish("id_name/message", MESSAGE_json)
self.mqtt.publish("id_name/cmd_ack", COMMAND_ACK_json)
self.mqtt.publish("id_name/apm_text", STATUS_TEXT_json)
self.mqtt.publish("id_name/mission_ack", MISSION_ACK_json)
```
4. For subscribing the command from back-end control webpage , you can change the MQTT broker topic name from ```MQTT.py```
```python=1
self.client.subscribe("id_name/cmd")
```
5. If you want to listen additional MAVLink Message, refer to the example code from Dronekit Github [:link:][create_attribute] 

***For example, GLOBAL_POSITION_INT ( #33 )*** 

First, add the custom classq and listener in ```my_vehicle.py``` 

[create_attribute]: https://github.com/dronekit/dronekit-python/blob/master/examples/create_attribute/create_attribute.py

```python=1
class GLOBAL_POSITION_INT(object):

    def __init__(self, time_boot_us=None, lat=None, lon=None, alt=None, relative_alt=None, vx=None, vy=None, vz=None, hdg=None):
        self.time_boot_us = time_boot_us
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.relative_alt = relative_alt
        self.vx = vx
        self.vy = vy
        self.vz = vz        
        self.hdg = hdg
        
    def __str__(self):
        GLOBAL_POSITION_INT_dict = {'lat':self.lat, 'lng':self.lon, 'alt':self.alt, 'relative_alt':self.relative_alt, 'heading': self.hdg}
        GLOBAL_POSITION_INT_json = json.dumps(GLOBAL_POSITION_INT_dict)
        return GLOBAL_POSITION_INT_json

```

```python=1
class MyVehicle(Vehicle):
    def __init__(self, *args):
        super(MyVehicle, self).__init__(*args)

        # GLOBAL_POSITION_INT
        self._GLOBAL_POSITION_INT = GLOBAL_POSITION_INT()
        @self.on_message('GLOBAL_POSITION_INT')
        def listener(self, name, message):

            self._GLOBAL_POSITION_INT.time_boot_us = message.time_boot_ms
            self._GLOBAL_POSITION_INT.lat = message.lat / 1.0e7
            self._GLOBAL_POSITION_INT.lon = message.lon / 1.0e7
            self._GLOBAL_POSITION_INT.alt = message.alt / 1000.0
            self._GLOBAL_POSITION_INT.relative_alt = message.relative_alt / 1000.0
            self._GLOBAL_POSITION_INT.vx = message.vx
            self._GLOBAL_POSITION_INT.vy = message.vy
            self._GLOBAL_POSITION_INT.vz = message.vz
            self._GLOBAL_POSITION_INT.hdg = message.hdg / 100

            self.notify_attribute_listeners('GLOBAL_POSITION_INT', self._GLOBAL_POSITION_INT)

```
And then add callback function in ```drone_msg.py```
```python=1
def GLOBAL_POSITION_INT_callback(self, self_, attr_name, value):
    self.location = json.loads(str(value))
```
Finally, use ***add_attribute_listener*** function in ```__init__.py```
```python=1
demo_drone = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle)
demo_drone.add_attribute_listener('GLOBAL_POSITION_INT', Drone_msg.GLOBAL_POSITION_INT_callback)
```
6. If you want to use addtional MAVLink command, pls refer to ```drone_command.py```, In most cases, you can use only ***COMMAND_LONG ( #76 )*** message to wrap the command you want to use and the parameters. MAVLink Command can be found in their offcial website [:link:][MAV_CMD] 

[MAV_CMD]: https://mavlink.io/en/messages/common.html#mav_commands

```python=1
def ARM_DISARM(self, is_armed):
    msg = self.vehicle.message_factory.command_long_encode(
                0, 0,   # target system, target component
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, # command
                0,          # confirmation
                is_armed, 0       # param 1.2
                ,0, 0, 0, 0, 0)   # param 3~7
    self.vehicle.send_mavlink(msg)
```
