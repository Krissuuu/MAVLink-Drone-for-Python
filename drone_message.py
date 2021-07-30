from __future__ import print_function
import json
import time

class Drone_message():

    def __init__(self, timestamp=None, location=None, battery=None, speed=None, attitude=None, gps_status=None, heartbeat=None,
                 cmd_ack=None, status_text=None, mission_ack=None):

        self.timestamp = timestamp
        self.location = location
        self.battery = battery
        self.speed = speed
        self.attitude = attitude
        self.gps_status = gps_status
        self.heartbeat = heartbeat
        self.cmd_ack = cmd_ack
        self.status_text = status_text
        self.mission_ack = mission_ack

    def GLOBAL_POSITION_INT_callback(self, self_, attr_name, value):
        self.location = json.loads(str(value))

    def SYS_STATUS_callback(self, self_, attr_name, value):
        self.battery = json.loads(str(value))

    def VFR_HUD_callback(self, self_, attr_name, value):
        self.speed = json.loads(str(value))

    def ATTITUDE_callback(self, self_, attr_name, value):
        self.attitude = json.loads(str(value))

    def GPS_RAW_INT_callback(self, self_, attr_name, value):
        self.gps_status = json.loads(str(value))

    def HEARTBEAT_callback(self, self_, attr_name, value):
        self.heartbeat = json.loads(str(value))

    def COMMAND_ACK_callback(self, self_, attr_name, value):
        self.cmd_ack = json.loads(str(value))

    def STATUS_TEXT_callback(self, self_, attr_name, value):
        self.status_text = json.loads(str(value))

    def MISSION_ACK_callback(self, self_, attr_name, value):
        self.mission_ack = json.loads(str(value))


    def DRONE_MESSAGE(self):
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        drone_msg_dict = {'timestamp':self.timestamp, 'location':self.location, 'battery':self.battery,
                        'speed':self.speed, 'attitude':self.attitude, 'gps_status':self.gps_status,
                        'heartbeat':self.heartbeat}
        return drone_msg_dict

    # def PRINT_MESSAGE(self):
    #     while True:
    #         MESSAGE = self.DRONE_MESSAGE()
    #         print(MESSAGE)
    #         time.sleep(1)
