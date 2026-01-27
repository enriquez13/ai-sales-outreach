import requests, os
from dotenv import load_dotenv

load_dotenv()

API = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def generate_email(lead):

    prompt = f"""
Write a professional B2B email.

Name: {lead.name}
Company: {lead.company}
Sector: {lead.category}
"""

    payload = {"inputs": prompt}

    r = requests.post(API, headers=HEADERS, json=payload)
    return r.json()[0]["generated_text"]
