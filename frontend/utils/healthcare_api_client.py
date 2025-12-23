import requests
from typing import Dict, Any

# --------------------------------
# Base URLs
# --------------------------------
BASE_URL = "http://127.0.0.1:8000"

DISEASE_API_BASE = f"{BASE_URL}/api/v1/disease"
READMISSION_API_BASE = f"{BASE_URL}/api/v1/readmission"
XRAY_API_URL = f"{BASE_URL}/api/v1/predictions/xray"


class HealthcareAPIClient:
    """Unified API client for Healthcare Backend"""

    # ----------------------------
    # Disease Prediction
    # ----------------------------
    @staticmethod
    def predict_disease(payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{DISEASE_API_BASE}/predict",
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Backend not reachable. Is FastAPI running?"}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # ----------------------------
    # Readmission Prediction
    # ----------------------------
    @staticmethod
    def predict_readmission(patient_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{READMISSION_API_BASE}/predict",
                json=patient_data,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # ----------------------------
    # X-ray Image Prediction
    # ----------------------------
    @staticmethod
    def predict_xray(image_file) -> Dict[str, Any]:
        files = {
            "file": (
                image_file.name,
                image_file,
                image_file.type if hasattr(image_file, "type") else "image/jpeg"
            )
        }

        try:
            response = requests.post(XRAY_API_URL, files=files, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # ----------------------------
    # Fetch Disease Records
    # ----------------------------
    @staticmethod
    def get_disease_records() -> Dict[str, Any]:
        try:
            response = requests.get(f"{DISEASE_API_BASE}/records", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    # ----------------------------
    # Health Check
    # ----------------------------
    @staticmethod
    def health_check() -> Dict[str, Any]:
        try:
            response = requests.get(BASE_URL, timeout=3)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy"
            }
        except requests.exceptions.RequestException:
            return {
                "status": "unhealthy",
                "error": "Backend not reachable"
            }


# --------------------------------
# Backward Compatibility Functions
# --------------------------------
def predict_disease_api(payload: Dict[str, Any]) -> Dict[str, Any]:
    return HealthcareAPIClient.predict_disease(payload)


def predict_xray(image_file) -> Dict[str, Any]:
    return HealthcareAPIClient.predict_xray(image_file)
