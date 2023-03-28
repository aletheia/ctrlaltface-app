import os
from os.path import abspath, join
import dlib
import logging
import cv2
import numpy as np

faces_path = abspath("./faces")


class FaceRecognition:
    def __init__(self):
        logging.info("Initializing face recognition")
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(
            abspath("./libs/shape_predictor_5_face_landmarks.dat"))
        self.facerec = dlib.face_recognition_model_v1(
            abspath("./libs/dlib_face_recognition_resnet_model_v1.dat"))
        self.faces = []
        self.face_names = []
        self.face_descriptors = []

    def encode_faces(self, image):
        # img = dlib.load_rgb_image(join(faces_path, image))
        if image is None:
            logging.error("Empty image")
            raise Exception("Empty image")

        faces_in_image = self.detector(image, 1)
        logging.info(
            "Found {} faces in image".format(len(faces_in_image)))
        if len(faces_in_image) > 0:
            shape = self.sp(image, faces_in_image[0])

            face_aligned = dlib.get_face_chip(image, shape)
            face_descriptor = np.array(self.facerec.compute_face_descriptor(
                face_aligned))
            return face_aligned, face_descriptor
        else:
            logging.error("No faces found in image")
            return None, None

    def load_faces(self):
        # load faces from faces folder
        for face in os.listdir(faces_path):
            if not face.startswith("."):
                logging.info("Loading face: {}".format(face))
                img = cv2.imread(join(faces_path, face))
                self.faces.append(self.encode_faces(img))
                self.face_names.append(face.split(".")[0])
        logging.info("Loaded {} faces".format(len(self.faces)))

    def compute_distance(self, face1_representation, face2_representation):
        # compute distance between two faces
        if face1_representation is None or face2_representation is None:
            raise Exception("One of the faces is not valid")
        euclidean_distance = face1_representation - face2_representation
        euclidean_distance = np.sum(np.multiply(
            euclidean_distance, euclidean_distance))
        euclidean_distance = np.sqrt(euclidean_distance)
        return euclidean_distance

    def recognize_face(self, image):
        # recognize face in image
        (face, descriptor) = self.encode_faces(image)
        index = -1
        if (face is not None):
            for (face, desc) in self.faces:
                dist = self.compute_distance(desc, descriptor)
                if dist < 0.6:
                    logging.info("Face recognized: {}".format(
                        self.face_names[index]))
                    return self.face_names[index]
                index += 1
        else:
            logging.error("No faces found")
            return None
