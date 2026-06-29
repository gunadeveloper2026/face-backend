import os
import cv2
import numpy as np
from deepface import DeepFace

DATASET_PATH = "app/static/employees"

employee_db = []

# Cache embeddings model usage
MODEL_NAME = "Facenet512"
DETECTOR = "opencv"


def load_faces():
    global employee_db
    employee_db = []

    if not os.path.exists(DATASET_PATH):
        print("Dataset folder not found")
        return

    for file in os.listdir(DATASET_PATH):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(DATASET_PATH, file)

        try:
            result = DeepFace.represent(
                img_path=path,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR,
                enforce_detection=False
            )

            if result and len(result) > 0:
                employee_db.append({
                    "name": os.path.splitext(file)[0],
                    "embedding": result[0]["embedding"]
                })

        except Exception as e:
            print(f"Error loading {file}: {e}")


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0

    return np.dot(a, b) / denom


def recognize_face(image_path):
    try:
        result = DeepFace.represent(
            img_path=image_path,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR,
            enforce_detection=False
        )

        if not result:
            return None, 0

        embedding = result[0]["embedding"]

        best_score = -1
        best_employee = None

        for emp in employee_db:
            score = cosine_similarity(embedding, emp["embedding"])

            if score > best_score:
                best_score = score
                best_employee = emp["name"]

        # threshold (you can tune this)
        if best_score > 0.65:
            return best_employee, float(best_score)

        return None, float(best_score)

    except Exception as e:
        print("Recognition error:", e)
        return None, 0