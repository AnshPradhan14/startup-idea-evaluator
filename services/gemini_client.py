import time
import requests

class GeminiClient:
    def __init__(self, api_key, model='gemini-2.5-flash'):
        self.api_key = api_key
        self.model = model
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        self.headers = {"Content-Type": "application/json"}

    def generate(self, prompt, retries=5, backoff_factor=2):
        """
        Calls Gemini API with exponential backoff to handle 503 or transient errors.
        """
        payload = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,   # Lower = more deterministic
                "topP": 0.8,
                "topK": 40
            }
        }

        for attempt in range(retries):
            resp = requests.post(
                f"{self.url}?key={self.api_key}",
                headers=self.headers,
                json=payload
            )

            # ✅ Success
            if resp.status_code == 200:
                return resp.json()

            # ⚠️ Retry on transient or overload errors
            if resp.status_code in (429, 500, 502, 503, 504):
                wait = backoff_factor ** attempt
                print(f"⚠️ Gemini API overloaded (status {resp.status_code}). Retrying in {wait}s...")
                time.sleep(wait)
                continue

            # ❌ Hard failure
            raise RuntimeError(f"Gemini API error: {resp.status_code}\n{resp.text}")

        raise RuntimeError(f"Gemini API failed after {retries} retries (last: {resp.status_code})")
