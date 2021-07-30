from time import sleep
from dronekit import connect
import threading

from my_vehicle import MyVehicle
from drone_command import Drone_command
from drone_message import Drone_message

import sys
from PyQt5.QtWidgets import QDialog, QApplication
from drone_control_UI import Ui_Form


class AppWindow(QDialog):
    def __init__(self, drone_cmd, drone_msg):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.drone_cmd = drone_cmd
        self.msg = drone_msg

        threaad = threading.Thread(target = self.Print_Drone_Message)
        threaad.setDaemon(True)
        threaad.start()

        self.ui.setmode.currentIndexChanged.connect(self.set_mode_Click)
        self.ui.arm.clicked.connect(self.arm_Click)
        self.ui.disarm.clicked.connect(self.disarm_Click)
        self.ui.takeoff.clicked.connect(self.takeoff_Click)
        self.ui.change_speed.clicked.connect(self.change_speed_Click)
        self.ui.change_yaw.clicked.connect(self.change_yaw_Click)
        self.ui.go.clicked.connect(self.goto_Click)
        self.show()

    def Print_Drone_Message(self):
        while True:
            drone_messgae_callback = self.msg.DRONE_MESSAGE()
            if drone_messgae_callback is not None:
                self.ui.display_timestamp.setText(str(drone_messgae_callback['timestamp']))

                heartbeat_dict = drone_messgae_callback['heartbeat']
                if heartbeat_dict is not None:
                    self.ui.display_flightmode.setText(str(drone_messgae_callback['heartbeat']['flight_mode']))

                    isArmed = str(drone_messgae_callback['heartbeat']['is_armed'])
                    if isArmed == "0":
                        self.ui.display_isarmed.setText("DISARMED")
                    else:
                        self.ui.display_isarmed.setText("ARMED")

                self.ui.display_location.setText(str(drone_messgae_callback['location']))
                self.ui.display_battery.setText(str(drone_messgae_callback['battery']))
                self.ui.display_speed.setText(str(drone_messgae_callback['speed']))
                self.ui.display_altitude.setText(str(drone_messgae_callback['attitude']))
                self.ui.display_gps.setText(str(drone_messgae_callback['gps_status']))
            sleep(1)

    def set_mode_Click(self):
        mode = self.ui.setmode.currentIndex()
        self.drone_cmd.SET_MODE(int(mode))
    def arm_Click(self):
        self.drone_cmd.ARM_DISARM(1)
    def disarm_Click(self):
        self.drone_cmd.ARM_DISARM(0)
    def takeoff_Click(self):
        self.drone_cmd.TAKEOFF(10)
    def change_speed_Click(self):
        speed = self.ui.edit_speed.toPlainText()
        self.drone_cmd.CHANGE_SPEED(float(speed))
    def change_yaw_Click(self):
        yaw = self.ui.edit_yaw.toPlainText()
        self.drone_cmd.CHANGE_YAW(int(yaw))
    def goto_Click(self):
        lat = self.ui.edit_lat.toPlainText()
        lng = self.ui.edit_lng.toPlainText()
        alt = self.ui.edit_alt.toPlainText()
        self.drone_cmd.GOTO(float(lat), float(lng), float(alt))

def connect_sitl():

    CONNECTION_STRING = '127.0.0.1:14551'
    print('Connecting to vehicle on: %s' % CONNECTION_STRING)

    drone = connect(CONNECTION_STRING, wait_ready=True, vehicle_class=MyVehicle)

    drone_cmd = Drone_command(vehicle=drone)
    drone_msg = Drone_message()

    drone.add_attribute_listener('GLOBAL_POSITION_INT', drone_msg.GLOBAL_POSITION_INT_callback)
    drone.add_attribute_listener('SYS_STATUS', drone_msg.SYS_STATUS_callback)
    drone.add_attribute_listener('VFR_HUD', drone_msg.VFR_HUD_callback)
    drone.add_attribute_listener('ATTITUDE', drone_msg.ATTITUDE_callback)
    drone.add_attribute_listener('GPS_RAW_INT', drone_msg.GPS_RAW_INT_callback)
    drone.add_attribute_listener('HEARTBEAT', drone_msg.HEARTBEAT_callback)
    drone.add_attribute_listener('COMMAND_ACK', drone_msg.COMMAND_ACK_callback)
    drone.add_attribute_listener('STATUSTEXT', drone_msg.STATUS_TEXT_callback)
    drone.add_attribute_listener('MISSION_ACK', drone_msg.MISSION_ACK_callback)

    return drone_cmd, drone_msg

if __name__ == '__main__':

    drone_cmd, drone_msg = connect_sitl()
    app = QApplication(sys.argv)
    w = AppWindow(drone_cmd, drone_msg)
    w.show()
    sys.exit(app.exec_())