import cv2
from face_recognition import FaceRecognition
from camera import Camera
from logic import Logic
import logging
import config

logging.basicConfig(filename=config.output_file_name, level=logging.INFO)


def main():

    logging.info("Starting face recognition...")
    logging.info('Started')

    logic = Logic()

    detector = FaceRecognition()
    detector.load_faces()

    camera = Camera()
    camera.start_capture()

    skip_step = False
    while True:
        if skip_step:
            skip_step = False
            continue
        frame = camera.get_frame()
        res = detector.recognize_face(frame)
        if res is not None:
            logic.recognize_face(res)
        skip_step = True


if __name__ == "__main__":
    main()
