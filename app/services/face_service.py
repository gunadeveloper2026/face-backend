import os
import cv2
import numpy as np
from deepface import DeepFace

DATASET_PATH = "app/static/employees"

employee_db = []


def load_faces():
    global employee_db

    employee_db = []

    for file in os.listdir(DATASET_PATH):

        path = os.path.join(DATASET_PATH, file)

        try:

            embedding = DeepFace.represent(
                img_path=path,
                model_name="Facenet512",
                detector_backend="opencv",
                enforce_detection=False
            )[0]["embedding"]

            employee_db.append({
                "name": file.split(".")[0],
                "embedding": embedding
            })

        except:
            pass


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def recognize_face(image_path):

    try:

        result = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet512",
            detector_backend="opencv",
            enforce_detection=False
        )

        if len(result) == 0:
            return None, 0

        embedding = result[0]["embedding"]

        best_score = -1
        best_employee = None

        for emp in employee_db:

            score = cosine_similarity(
                embedding,
                emp["embedding"]
            )

            if score > best_score:

                best_score = score
                best_employee = emp["name"]

        if best_score > 0.65:

            return best_employee, best_score

        return None, best_score

    except Exception as e:

        print(e)

        return None, 0