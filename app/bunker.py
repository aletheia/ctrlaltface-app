from shelly_utils import ShellyDevice
import pyttsx3
import config
from os.path import abspath, join
import logging

import multiprocessing as mp

import time


def announceWorker(queue):
    synthesizer = pyttsx3.init()
    while True:
        logging.info("Waiting for message")
        message = queue.get()
        synthesizer.say(message)
        synthesizer.runAndWait()
        synthesizer.stop()


class Bunker:
    def __init__(self) -> None:
        self.device = ShellyDevice(
            config.shelly_ip_address, channels=config.shelly_channels)
        self.forward_direction = True
        self.synthesizer = pyttsx3.init()
        self.last_action_time = time.time()
        self.last_unknown_time = time.time()

        logging.info("Starting bunker face monitoring")
        self.queue = mp.Queue()
        self.process = mp.Process(target=announceWorker, args=(self.queue,))
        self.process.start()
        self.queue.put('Starting bunker face monitoring')

    def announce_opening(self, user_name):
        # self.synthesizer.say(
        #     config.face_recognition_message.format(user_name))
        # self.synthesizer.say('Opening the bunker')
        # self.synthesizer.runAndWait()
        # self.synthesizer.stop()
        self.queue.put(config.face_recognition_message.format(user_name))
        self.queue.put('Opening the bunker')

    def announce_closing(self, user_name):
        # self.synthesizer.say(
        #     config.face_recognition_message.format(user_name))
        # self.synthesizer.say('Closing the bunker')
        # self.synthesizer.runAndWait()
        # self.synthesizer.stop()
        self.queue.put(config.face_recognition_message.format(user_name))
        self.queue.put('Closing the bunker')

    def announce_unknown(self):
        current_time = time.time()
        delta = abs(current_time - self.last_unknown_time)
        if delta > config.sleep_time:
            logging.info("Activating bunker")
            # self.synthesizer.say(config.face_unknown_message)
            # self.synthesizer.runAndWait()
            # self.synthesizer.stop()
            # self.last_unknown_time = time.time()
            self.queue.put(config.face_unknown_message)

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
