import requests
import json

API_URL = "http://localhost:8000/query"
BEARER_TOKEN = "8c2123a098ae17e61c519f9c84b0eb4fa35074d106c68f2bc8afc44ab837c0a1"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}
payload = {
    "questions": ["Are dental treatments or surgeries covered?"]
}

print("Querying the knowledge base...")
response = requests.post(API_URL, headers=headers, json=payload)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
else:
    print(response.text)