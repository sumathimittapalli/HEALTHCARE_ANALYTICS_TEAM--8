from app.ml_models.medicine_predict_model import MedicineRecommender

MODEL = None

def load_medicine_model():
    global MODEL
    if MODEL is None:
        MODEL = MedicineRecommender()
    return MODEL
