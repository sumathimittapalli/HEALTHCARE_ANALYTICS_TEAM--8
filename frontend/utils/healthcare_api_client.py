import requests
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

DISEASE_API_BASE = f"{BASE_URL}/api/v1/disease"
READMISSION_API_BASE = f"{BASE_URL}/api/v1/readmission"
XRAY_API_URL = f"{BASE_URL}/api/v1/predictions/xray"
MEDICINE_API_URL = f"{BASE_URL}/medicine"


class HealthcareAPIClient:
    """Unified API client for Healthcare Backend"""

    @staticmethod
    def predict_disease(payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            r = requests.post(f"{DISEASE_API_BASE}/predict", json=payload, timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def predict_readmission(payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            r = requests.post(f"{READMISSION_API_BASE}/predict", json=payload, timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def predict_xray(image_file) -> Dict[str, Any]:
        files = {"file": (image_file.name, image_file, "image/jpeg")}
        try:
            r = requests.post(XRAY_API_URL, files=files, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def recommend_medicine(payload: Dict[str, Any]):
        try:
            r = requests.post(f"{MEDICINE_API_URL}/recommend", json=payload, timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def health_check():
        try:
            r = requests.get(BASE_URL, timeout=3)
            return {"status": "healthy" if r.status_code == 200 else "unhealthy"}
        except Exception:
            return {"status": "unhealthy"}


# Backward compatibility
def predict_xray(image_file):
    return HealthcareAPIClient.predict_xray(image_file)
