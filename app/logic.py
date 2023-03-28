import logging
import config


class Logic:
    def __init__(self):
        self.recognized_faces = 0
        self.faces_treshold = config.counter_threshold

    def recognize_face(self, name):
        self.recognized_faces += 1
        if self.recognized_faces >= self.faces_treshold:
            self.recognized_faces = 0
            logging.info(f"Logic recognized face {name}. Triggering action...")
            # do something here
