import cv2
from face_recognition import FaceRecognition
from camera import FrameGrabber
from logic import Logic
import logging

from observers import Observer

from shelly_utils import ShellyDevice
import config

# logging.basicConfig(filename=config.output_file_name, level=logging.INFO)
logging.basicConfig(level=logging.INFO)


class g(Observer):
    def update(self, frame):
        logging.info("Got frame")


def main():

    logging.info("Starting face recognition...")
    logging.info('Started')

    logic = Logic()

    camera = FrameGrabber()
    camera.register(logic)
    cam_indexes = camera.list_camera_indexes()
    camera.init_capture(cam_indexes[0])
    camera.run()


if __name__ == "__main__":
    main()
