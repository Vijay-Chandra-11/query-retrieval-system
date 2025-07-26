import requests
import io
from pypdf import PdfReader

def download_pdf(url: str) -> bytes:
    print(f"Downloading PDF from {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("Download complete.")
    return response.content

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    print("Extracting text from PDF...")
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    print(f"Extracted {len(text)} characters.")
    return text