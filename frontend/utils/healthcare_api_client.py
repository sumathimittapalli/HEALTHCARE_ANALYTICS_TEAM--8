import requests
from typing import Dict, Any

# Base URLs for different API endpoints
DISEASE_API_BASE = "http://127.0.0.1:8000/api/v1/disease"
READMISSION_API_BASE = "http://127.0.0.1:8000/api/v1/readmission"

class HealthcareAPIClient:
    """Unified API client for healthcare analytics endpoints"""
    
    @staticmethod
    def predict_disease(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls the FastAPI /disease/predict endpoint and returns the JSON response.
        Returns a dict with prediction or error message.
        """
        try:
            response = requests.post(f"{DISEASE_API_BASE}/predict", json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
            return {"error": str(http_err)}
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error: {conn_err}")
            return {"error": "Could not connect to backend. Make sure FastAPI is running."}
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error: {timeout_err}")
            return {"error": "Request timed out."}
        except requests.exceptions.RequestException as req_err:
            print(f"Request exception: {req_err}")
            return {"error": str(req_err)}
    
    @staticmethod
    def predict_readmission(patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send patient data as POST request to readmission endpoint and get prediction.
        """
        try:
            response = requests.post(f"{READMISSION_API_BASE}/predict", json=patient_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("API request failed:", e)
            return {"error": str(e)}
    
    @staticmethod
    def get_disease_records() -> Dict[str, Any]:
        """Get all disease prediction records"""
        try:
            response = requests.get(f"{DISEASE_API_BASE}/records")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("API request failed:", e)
            return {"error": str(e)}
    
    @staticmethod
    def health_check() -> Dict[str, Any]:
        """Check if the backend API is running"""
        try:
            response = requests.get("http://127.0.0.1:8000/")
            return {"status": "healthy" if response.status_code == 200 else "unhealthy"}
        except requests.exceptions.RequestException:
            return {"status": "unhealthy", "error": "Backend not reachable"}

# Backward compatibility functions
def predict_disease_api(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy function for backward compatibility"""
    return HealthcareAPIClient.predict_disease(payload)