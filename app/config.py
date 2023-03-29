import os
import json
from os.path import abspath, join

config_path = abspath('./config.json')
if not os.path.exists(config_path):
    raise Exception("Config file not found")

with open(config_path) as f:
    config = json.load(f)


output_file_name = config["outputFileName"]
dlib_landmarks_file = config["dlibLandmarksFile"]
dlib_face_recognition_model_file = config["dlibFaceRecognitionModelFile"]
faces_path = config["facesPath"]
shelly_ip_address = config["shellyIpAddress"]
shelly_type = config["shellyType"]
counter_threshold = config["counterThreshold"]
sleep_time = config["sleepTime"]
