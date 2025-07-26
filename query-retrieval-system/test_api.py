import requests
import json

API_URL = "http://localhost:8000/hackrx/run"
BEARER_TOKEN = "8c2123a098ae17e61c519f9c84b0eb4fa35074d106c68f2bc8afc44ab837c0a1"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "documents": "https://hackrx.in/policies/BAJHLIP23020V012223.pdf",
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for Pre-Existing Diseases?",
        "Are maternity expenses covered under this policy?",
        "Is there a waiting period for cataract surgery?",
        "Are the medical expenses for a living organ donor covered?",
        "What is the Cumulative Bonus for a claim-free year?",
        "Is there a benefit for an Annual Preventive Health Check-up?",
        "How does this policy define a 'Hospital'?",
        "What is the coverage for Ayurvedic / Homeopathic hospitalization?",
        "Are there any limits on room rent for domestic (in-India) hospitalization?"
    ]
}

print("Sending request to the API...")
response = requests.post(API_URL, headers=headers, json=payload)

print(f"Status Code: {response.status_code}")
print("--- Response JSON ---")
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
else:
    # Print the detailed error from the server if something goes wrong
    print(response.text)