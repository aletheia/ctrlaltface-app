import cv2
import logging
from observers import Observable


class FrameGrabber(Observable):
    def __init__(self):
        super().__init__()
        self.video_capture = None

    def __del__(self):
        self.video_capture.release()

    def list_camera_indexes(self):
        index = 0
        available_cameras = []
        while index < 10:
            logging.info("Checking camera {}".format(index))
            try:
                cap = cv2.VideoCapture(index)
                if cap is not None and cap.isOpened():
                    print("Camera {} is available".format(index))
                    available_cameras.append(index)
                cap.release()
                cap = None
            except:
                pass
            index += 1

        logging.info("Found available cameras: {}".format(available_cameras))
        if len(available_cameras) == 0:
            logging.error("No camera found")
            raise Exception("No camera found")
        return available_cameras

    def init_capture(self, camera_index):
        self.video_capture = cv2.VideoCapture(camera_index)
        if self.video_capture is None or not self.video_capture.isOpened():
            logging.error("Failed to open camera")
            raise Exception("Failed to open camera")

    def get_frame(self):
        success, image = self.video_capture.read()
        if (success):
            return image
        else:
            logging.error("Failed to get frame")
            raise Exception("Failed to get frame")

    def run(self):
        logging.info("Starting frame grabber")
        cv2.destroyAllWindows()
        while True:
            try:
                frame = self.get_frame()

                self.notify(frame)
            except Exception as e:
                logging.error("Failed to get frame: {}".format(e))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
