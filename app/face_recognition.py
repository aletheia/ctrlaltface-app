import os
from os.path import abspath, join
import dlib
import logging
import cv2
import numpy as np
import config
from time import time

faces_path = abspath(config.faces_path)


class FaceRecognition():
    def __init__(self):
        logging.info("Initializing face recognition")
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(
            abspath(config.dlib_landmarks_file))
        self.facerec = dlib.face_recognition_model_v1(
            abspath(config.dlib_face_recognition_model_file))
        self.faces = []

    def encode_faces(self, image):
        face_encoded = None, None
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
            face_encoded = (face_aligned, face_descriptor, faces_in_image)
            return face_encoded
        else:
            logging.error("No faces found in image")
        return None, None, None

    def load_faces(self):
        # load faces from faces folder
        for face_file in os.listdir(faces_path):
            if not face_file.startswith("."):
                logging.info("Loading face: {}".format(face_file))
                img = cv2.imread(join(faces_path, face_file))
                face, desc, _ = self.encode_faces(img)
                name = face_file.split(".")[0]
                self.faces.append((face, desc, name))

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

        (face, descriptor, faces_in_image) = self.encode_faces(image)

        face_recognized = False
        face_name = None
        if (face is not None):
            if (config.save_detected_faces):
                ts = time()
                save_path = abspath("./tmp")
                cv2.imwrite(f"{save_path}/{face_name}-{ts}.png", image)

            minimum_distance = None
            minimum_distance_index = -1
            most_similar_face = None

            for (face, desc, name) in self.faces:

                dist = self.compute_distance(desc, descriptor)
                # logging.info(f"Distance for {name}: {dist}")
                if minimum_distance == None or dist < minimum_distance:
                    minimum_distance = dist
                    most_similar_face = (face, desc, name)

            if minimum_distance < 0.559:

                face, desc, name = most_similar_face

                logging.info(f"Face recognized: {name}")
                face_recognized = True  # detected
            else:
                #    logging.info("Face not recognized")
                face_recognized = False  # undetected

            face, desc, name = most_similar_face

            return (face_recognized, name, faces_in_image)
        else:
            logging.info("No faces found")
            return None, None, None
