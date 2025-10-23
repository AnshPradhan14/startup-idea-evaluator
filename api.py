import os
from services.gemini_client import GeminiClient
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", None)
client = GeminiClient(api_key=GEMINI_KEY, model="gemini-2.5-flash")
resp = client.generate("Say hello in one sentence.")
print(resp)
