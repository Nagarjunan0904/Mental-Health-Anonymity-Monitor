import os
import requests

API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def score_text(text: str) -> dict:
    if not API_KEY:
        raise RuntimeError("PERSPECTIVE_API_KEY not set")

    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "IDENTITY_ATTACK": {},
        }
    }

    resp = requests.post(API_URL, params={"key": API_KEY}, json=data, timeout=15)
    resp.raise_for_status()
    result = resp.json()

    scores = {}
    for attr in ["TOXICITY", "INSULT", "IDENTITY_ATTACK"]:
        scores[attr.lower()] = result["attributeScores"][attr]["summaryScore"]["value"]

    return scores

if __name__ == "__main__":
    
    text = "I feel really sad and hopeless today."
    print(score_text(text))
