import numpy as np
from PIL import Image
import io
from sqlalchemy.orm import Session
from app.ml_models.model_loader import load_xray_model
from app.models.xray_prediction import XRayPrediction

LABELS = ["Normal", "Pneumonia"]
MODEL_NAME = "xray_model_v1"

async def predict_and_store_xray(
    file,
    db: Session
):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    model = load_xray_model()
    preds = model.predict(image)[0]

    idx = int(np.argmax(preds))
    label = LABELS[idx]
    confidence = float(preds[idx])

    record = XRayPrediction(
        image_name=file.filename,
        prediction=label,
        confidence=confidence,
        model_name=MODEL_NAME
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
