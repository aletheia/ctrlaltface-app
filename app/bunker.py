from shelly_utils import ShellyDevice
import pyttsx3
import config
from os.path import abspath, join
import logging
from subprocess import call

import time


class Bunker:
    def __init__(self) -> None:
        self.device = ShellyDevice(
            config.shelly_ip_address, channels=config.shelly_channels)
        self.forward_direction = True
        self.synthesizer = pyttsx3.init()
        self.last_action_time = time.time()
        self.last_unknown_time = time.time()

    def announce_opening(self, user_name):
        self.synthesizer.say(
            config.face_recognition_message.format(user_name))
        self.synthesizer.say('Opening the bunker')
        self.synthesizer.runAndWait()
        self.synthesizer.stop()

    def announce_closing(self, user_name):
        self.synthesizer.say(
            config.face_recognition_message.format(user_name))
        self.synthesizer.say('Closing the bunker')
        self.synthesizer.runAndWait()
        self.synthesizer.stop()

    def announce_unknown(self):
        current_time = time.time()
        delta = abs(current_time - self.last_unknown_time)
        if delta > config.sleep_time:
            logging.info("Activating bunker")
            self.synthesizer.say(config.face_unknown_message)
            self.synthesizer.runAndWait()
            self.synthesizer.stop()
            self.last_unknown_time = time.time()

    def activate(self, user_name):
        current_time = time.time()
        delta = abs(current_time - self.last_action_time)
        if delta > config.sleep_time:
            logging.info("Activating bunker")

            if self.forward_direction:
                self.announce_opening(user_name)
                logging.info("ufff")
                if config.shelly_type == "roller":
                    res = self.device.openRoller()
                elif config.shelly_type == "relay":
                    res = self.device.switchOn()
                else:
                    logging.error("Unknown shelly type")
            else:
                self.announce_closing(user_name)
                logging.info("dsdssdsd")
                if config.shelly_type == "roller":
                    res = self.device.closeRoller()
                elif config.shelly_type == "relay":
                    res = self.device.switchOff()
                else:
                    logging.error("Unknown shelly type")
            logging.info(f"Logic triggered action. Result: {res}")
            self.forward_direction = not self.forward_direction

            self.last_action_time = time.time()
        else:
            logging.info(f"Skipping for {delta} seconds")
