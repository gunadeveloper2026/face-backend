# services/face_register.py

import face_recognition
import pickle

def create_face_encoding(image_path):

    image = face_recognition.load_image_file(image_path)

    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return None

    return encodings[0]