import requests

def analyze_text(text):
    payload = {
        "text": text,
        "language": "en",
        "entities": ["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS"],  # 根据需要添加
        "score_threshold": 0.5
    }
    response = requests.post("http://presidio-analyzer:3000/analyze", json=payload)
    response.raise_for_status()
    return response.json()
