import os
from tensorflow.keras.models import load_model

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "xray_model.h5"
)

_model = None

def load_xray_model():
    global _model

    if _model is not None:
        return _model

    print("🔍 Looking for model at:", MODEL_PATH)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"xray_model.h5 not found at {MODEL_PATH}")

    _model = load_model(MODEL_PATH)
    print("✅ X-ray model loaded successfully")
    return _model
