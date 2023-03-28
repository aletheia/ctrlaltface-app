import cv2
from face_recognition import FaceRecognition
from camera import Camera
import logging


def main():
    print("Starting face recognition...")
    print("Press 'q' to quit.")
    logging.basicConfig(filename='output.log', level=logging.INFO)
    logging.info('Started')

    detector = FaceRecognition()
    detector.load_faces()

    camera = Camera()
    camera.start_capture()

    while True:
        frame = camera.get_frame()
        res = detector.recognize_face(frame)


if __name__ == "__main__":
    main()
