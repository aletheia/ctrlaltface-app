import logging
import config

from time import sleep
from bunker import Bunker
from face_recognition import FaceRecognition
from observers import Observer


class Logic (Observer):
    def __init__(self):
        self.recognized_faces = 0
        self.faces_treshold = config.counter_threshold
        self.bunker = Bunker()
        self.detector = FaceRecognition()
        self.detector.load_faces()

    def recognize_face(self, frame):
        res, name = self.detector.recognize_face(frame)
        if res == 1:
            self.recognized_faces += 1
            if self.recognized_faces >= self.faces_treshold:
                self.recognized_faces = 0
                logging.info(
                    f"Logic recognized face {name}. Triggering action...")
                self.bunker.activate(name)
                # sleep(config.sleep_time)
        elif res == 0:
            logging.info("Found a face, but not recognized")
            self.recognized_faces = 0
            self.bunker.announce_unknown()
        else:
            self.recognized_faces = 0
            logging.info("Logic: No faces found")

    def process_frame(self, frame):
        self.recognize_face(frame)

    def update(self, frame):
        self.process_frame(frame)
