import logging
import config

from time import sleep
from bunker import Bunker
from face_recognition import FaceRecognition
from observers import Observer
from dlib_utils import convert_and_trim_bb
import cv2


class Logic (Observer):
    def __init__(self):
        self.recognized_faces = []
        self.faces_treshold = config.counter_threshold
        self.bunker = Bunker()
        self.detector = FaceRecognition()
        self.detector.load_faces()

    def recognize_face(self, frame):

        isFound, face_name, faces_in_image = self.detector.recognize_face(
            frame)

        if isFound is not None:
            if isFound is True:
                if (config.use_video):
                    boxes = [convert_and_trim_bb(frame, r)
                             for r in faces_in_image]

                    for (x, y, w, h) in boxes:
                        # draw the bounding box on our image
                        cv2.rectangle(frame, (x, y), (x + w, y + h),
                                      (0, 255, 0), 2)

                self.recognized_faces.append(face_name)
                if len(self.recognized_faces) >= self.faces_treshold:
                    self.recognized_faces = []
                    logging.info(
                        f"Logic recognized face {face_name}. Triggering action...")
                    self.bunker.activate(face_name)

            else:
                logging.info("Found a face, but not recognized")
                self.recognized_faces = []
                self.bunker.announce_unknown()
        else:
            self.recognized_faces = []
            logging.info("Logic: No faces found")

        if config.use_video:
            cv2.imshow('image', frame)

    def process_frame(self, frame):
        self.recognize_face(frame)

    def update(self, frame):
        self.process_frame(frame)
