import requests
import json
import logging


class ShellyDevice:
    def __init__(self, ip, username=None, password=None, channels=[0]):
        self.ip = ip
        self.username = username
        self.password = password
        self.channels = channels

    def get_status(self):
        url = f"http://{self.ip}/status"
        response = requests.get(url, auth=(self.username, self.password))
        return response.json()

    def set_relay(self, relay, state):
        url = f"http://{self.ip}/relay/{relay}?turn={state}"
        response = requests.get(url, auth=(self.username, self.password))
        return response.json()

    def set_roller(self, roller, state):
        url = f"http://{self.ip}/roller/{roller}?go={state}"
        response = requests.get(url, auth=(self.username, self.password))
        return response.json()

    def openRoller(self):
        logging.info("Opening roller")
        res = self.set_roller(0, "open")
        return res

    def closeRoller(self):
        logging.info("Closing roller")
        res = self.set_roller(0, "close")
        return res

    def switchOn(self, channel=None):
        logging.info("Switching on")
        if channel is None:
            for channel in self.channels:
                res = self.set_relay(channel, "on")
        else:
            res = self.set_relay(channel, "on")
        return res

    def switchOff(self, channel=None):
        logging.info("Switching off")
        if channel is None:
            for channel in self.channels:
                res = self.set_relay(channel, "off")
        else:
            res = self.set_relay(channel, "off")
        return res
