from dronekit import connect
import threading

from my_vehicle import MyVehicle
from drone_command import Drone_command
from drone_msg import Drone_message
from MQTT import MQTT

connection_string = '127.0.0.1:14551'
print('Connecting to vehicle on: %s' % connection_string)
demo_drone = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle)

Drone_cmd = Drone_command(vehicle = demo_drone)
mqtt = MQTT(vehicle = Drone_cmd)
Drone_msg = Drone_message(vehicle = demo_drone, mqtt = mqtt)

demo_drone.add_attribute_listener('GLOBAL_POSITION_INT', Drone_msg.GLOBAL_POSITION_INT_callback)
demo_drone.add_attribute_listener('SYS_STATUS', Drone_msg.SYS_STATUS_callback)
demo_drone.add_attribute_listener('VFR_HUD', Drone_msg.VFR_HUD_callback)
demo_drone.add_attribute_listener('ATTITUDE', Drone_msg.ATTITUDE_callback)
demo_drone.add_attribute_listener('GPS_RAW_INT', Drone_msg.GPS_RAW_INT_callback)
demo_drone.add_attribute_listener('HEARTBEAT', Drone_msg.HEARTBEAT_callback)
demo_drone.add_attribute_listener('COMMAND_ACK', Drone_msg.COMMAND_ACK_callback)
demo_drone.add_attribute_listener('STATUSTEXT', Drone_msg.STATUS_TEXT_callback)
demo_drone.add_attribute_listener('MISSION_ACK', Drone_msg.MISSION_ACK_callback)

t = threading.Thread(target = Drone_msg.Publish_MESSAGE)
t.start()