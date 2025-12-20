import requests

BASE = "http://127.0.0.1:8000/disease"

def predict_disease_api(payload: dict):
    """
    Calls the FastAPI /disease/predict endpoint and returns the JSON response.
    Returns a dict with prediction or error message.
    """
    try:
        r = requests.post(f"{BASE}/predict", json=payload, timeout=5)
        r.raise_for_status()  # Raises an HTTPError for 4xx/5xx responses
        return r.json()
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
