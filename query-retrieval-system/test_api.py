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
print("--- Response ---")
if response.status_code == 200:
    data = response.json()
    for i, item in enumerate(data['answers']):
        print(f"\n--- Answer #{i+1} ---")
        
        # This block checks if the answer is a JSON string and parses it for clean printing
        try:
            answer_data = json.loads(item['answer'])
            print(f"Answer: {answer_data.get('answer', item['answer'])}")
            print(f"Reasoning: {answer_data.get('reasoning', 'N/A')}")
        except (json.JSONDecodeError, TypeError):
            print(f"Answer: {item['answer']}")

        print("Sources:")
        if item['sources']:
            for source in item['sources']:
                print(f"  - Page {source.get('page', 'N/A')}: '{source.get('content', '')[:80].strip()}...'")
        else:
            print("  - No sources found.")
else:
    print(response.text)