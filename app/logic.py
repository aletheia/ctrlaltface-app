import logging
import config
from shelly_utils import ShellyDevice
from time import sleep
import pyttsx3


class Logic:
    def __init__(self):
        self.recognized_faces = 0
        self.faces_treshold = config.counter_threshold
        self.device = ShellyDevice(config.shelly_ip_address)
        self.forward_direction = True
        self.synthesizer = pyttsx3.init()

    def recognize_face(self, name):
        self.recognized_faces += 1
        if self.recognized_faces >= self.faces_treshold:
            self.recognized_faces = 0
            logging.info(f"Logic recognized face {name}. Triggering action...")
            # do something here
            if self.forward_direction:
                # status = "on"
                self.synthesizer.say(
                    f"Face detected. Wellcome {name}! Opening the door...")
                self.synthesizer.runAndWait()
                self.synthesizer.stop()
                status = "open"
            else:
                # status = "off"
                self.synthesizer.say(
                    f"Face detected. Wellcome {name}! Now closing the door...")
                self.synthesizer.runAndWait()
                self.synthesizer.stop()
                status = "close"
            # res = self.device.set_relay(0, status)
            # res = self.device.set_relay(1, status)
            res = self.device.set_roller(0, status)
            self.forward_direction = not self.forward_direction
            logging.info(f"Logic triggered action. Result: {res}")
            sleep(config.sleep_time)
