import cv2
import logging

logging.basicConfig(filename='output.log', level=logging.INFO)


class Camera:
    def __init__(self):
        self.video_capture = None
        # self.detect_camera()

    def __del__(self):
        self.video_capture.release()

    def detect_camera(self):
        available_cameras = self.returnCameraIndexes()
        logging.info("Available cameras: {}".format(available_cameras))
        if len(available_cameras) > 0:
            self.video_capture = cv2.VideoCapture(available_cameras[0])
            logging.info("Using camera {}".format(available_cameras[0]))

    def returnCameraIndexes(self):
        index = 0
        arr = []
        while index < 10:
            logging.info("Checking camera {}".format(index))
            cap = cv2.VideoCapture(index)
            if cap is not None or cap.isOpened():
                arr.append(index)
            cap.release()
            index += 1
        return arr

    def start_capture(self):
        self.video_capture = cv2.VideoCapture(1)
        process_this_frame = True

    def get_frame(self):
        success, image = self.video_capture.read()
        if (success):
           # Resize frame of video to 1/4 size for faster face recognition processing
            # small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            # rgb_small_frame = small_frame[:, :, ::-1]
            return image
