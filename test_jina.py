import os
import requests
from dotenv import load_dotenv

load_dotenv()

response = requests.post(
    "https://api.jina.ai/v1/embeddings",
    headers={
        "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}",
        "Content-Type": "application/json",
    },
    json={
        "model": "jina-embeddings-v3",
        "input": "Hello world",
    },
)

print(response.status_code)
print(response.text)