# MAVLink Drone for Python

- [Build ArduPilot SITL](#A)
- [Control Program](#B)
- [Reference](#C)

## *<a id="A">Build ArduPilot SITL</a>*
1. ***If you use Linux pls skip this step***, Install WSL (Win10 Subsystem).
2. Follow https://ardupilot.org/dev/docs/building-setup-linux.html#building-setup-linux to set up the SITL environment.
3. Follow https://github.com/ArduPilot/ardupilot/blob/master/BUILD.md to build the SITL source code. ***I use ./waf configure --board sitl***
4. ***If you use Linux pls skip this step***, Download https://sourceforge.net/projects/vcxsrv/ to visualize the Linux windows.
5. Input the command ***<sim_vehicle.py -v ArduCopter --console>*** on WSL terminal to run SITL. ***Input command <sim_vehicle.py -h> to see how to use the exist parameters.***
6. Open ***Mission Planner*** or ***QGroundControl*** to control and monitor the virtual drone.


## *<a id="B">Control Program</a>*

### Prerequisites
```
pip install dronekit
```
```
pip install pyqt5==5.10.1
pip install pyqt5-tools==5.9.0.1.2
```

### How to use
★ Run Ardupilot SITL by using this command ***sim_vehicle.py -v ArduCopter --console --custom-location=25.043014,121.536216,10,90*** on Linux terminal.

![](https://i.imgur.com/0aSJuM0.jpg)

★ Run ```__init__.py``` 

![](https://i.imgur.com/gT2Sa7Y.png)

1. ***If the connection between Python and SITL is successful***, you will see drone's message (Timestamp / Flight Mode / Location ...).
2. You can change ***flight mode (STABILIZE / ACRO / AUTO / GUIDED...)*** using the drop-down menu.
3. You can make drone ***ARM / DISARM / TAKEOFF*** using the corresponding button.
4. You can ***change the drone's flight speed*** using the ***"CHANGE SPEED" button*** after you input the flight speed you want.
5. You can ***change the drone's yaw angle*** using the ***"CHANGE YAW" button*** after you input the yaw angle you want.
6. You can let the drone ***fly to the destination*** you want, you have to input ***latitude / longitude / altitude*** and the press the ***"GOTO" button***.

**★Please change the flght mode to "GUIDED" before you control the drone.**
### Reference
★ If you want to modify the IP & port of ArduPilot SITL. You can change the code from ```__init__.py```.
```java=0
CONNECTION_STRING = '127.0.0.1:14551'
print('Connecting to vehicle on: %s' % CONNECTION_STRING)
drone = connect(CONNECTION_STRING, wait_ready=True, vehicle_class=MyVehicle)
```
★ If you want to listen additional MAVLink Message, refer to the example code from [Dronekit Github.](https://github.com/dronekit/dronekit-python/blob/master/examples/create_attribute/create_attribute.py)

***For example, GLOBAL_POSITION_INT ( #33 )*** 

First, add the custom classq and listener in ```my_vehicle.py``` 

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
And then add callback function in ```drone_message.py```
```python=1
def GLOBAL_POSITION_INT_callback(self, self_, attr_name, value):
    self.location = json.loads(str(value))
```
Finally, use ***add_attribute_listener*** function in ```__init__.py```
```python=1
drone = connect(CONNECTION_STRING, wait_ready=True, vehicle_class=MyVehicle)
drone_msg = Drone_message(vehicle=drone, rabbitmq=rabbitmq_producer)
drone.add_attribute_listener('GLOBAL_POSITION_INT', drone_msg.GLOBAL_POSITION_INT_callback)
```
★ If you want to use addtional MAVLink command, pls refer to ```drone_command.py```, In most cases, you can use only ***COMMAND_LONG ( #76 )*** message to wrap the command you want to use and the parameters. MAVLink Command can be found in [MAVLink offcial website.](https://mavlink.io/en/messages/common.html#mav_commands)

```python=1
def ARM_DISARM(self, is_armed):
    msg = self.vehicle.message_factory.command_long_encode(
                0, 0,                                         # target system, target component
                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, # command
                0,                                            # confirmation
                is_armed, 0                                   # param 1~2
                ,0, 0, 0, 0, 0)                               # param 3~7
    self.vehicle.send_mavlink(msg)
```

## *<a id="C">Reference</a>*

1. https://github.com/dronekit/dronekit-python

