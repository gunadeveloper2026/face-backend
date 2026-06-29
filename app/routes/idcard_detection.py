from fastapi import APIRouter, UploadFile, File
from ultralytics import YOLO
import cv2
import numpy as np

router = APIRouter()

model = YOLO("models/best.pt") # trained ID-card model

@router.post("/detect-id-card")
async def detect_id_card(file: UploadFile = File(...)):

    contents = await file.read()

    nparr = np.frombuffer(contents, np.uint8)

    frame = cv2.imdecode(
        nparr,
        cv2.IMREAD_COLOR
    )

    results = model(frame)

    id_card_found = False

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])

            label = model.names[cls]

            if label == "id_card":
                id_card_found = True

    return {
        "idCardDetected": id_card_found
    }