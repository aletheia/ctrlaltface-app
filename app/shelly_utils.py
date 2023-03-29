import requests
import json


class ShellyDevice:
    def __init__(self, ip, username=None, password=None):
        self.ip = ip
        self.username = username
        self.password = password

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
