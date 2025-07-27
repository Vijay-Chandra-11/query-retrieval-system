import requests

API_URL = "http://localhost:8000/upload"
BEARER_TOKEN = "8c2123a098ae17e61c519f9c84b0eb4fa35074d106c68f2bc8afc44ab837c0a1"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}
payload = {
    "document_url": "https://hackrx.in/policies/BAJHLIP23020V012223.pdf"
}

print("Uploading and processing document...")
response = requests.post(API_URL, headers=headers, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")