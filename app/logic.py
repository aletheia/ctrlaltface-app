import logging
import config
from shelly_utils import ShellyDevice
from time import sleep


class Logic:
    def __init__(self):
        self.recognized_faces = 0
        self.faces_treshold = config.counter_threshold
        self.device = ShellyDevice(config.shelly_ip_address)
        self.forward_direction = True

    def recognize_face(self, name):
        self.recognized_faces += 1
        if self.recognized_faces >= self.faces_treshold:
            self.recognized_faces = 0
            logging.info(f"Logic recognized face {name}. Triggering action...")
            # do something here
            if self.forward_direction:
                status = "on"
            else:
                status = "off"
            res = self.device.set_relay(0, status)
            # res = self.device.set_relay(1, status)
            self.forward_direction = not self.forward_direction
            logging.info(f"Logic triggered action. Result: {res}")
            sleep(config.sleep_time)
