import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

leads_db = [
    {"id": 1, "name": "Juan Perez", "company": "Empresa Test"}
]

@app.get("/leads")
async def get_leads():
    return leads_db


@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):

    lead = next((l for l in leads_db if l["id"] == lead_id), None)

    if not lead:
        return {"email": "Cliente no encontrado"}

    prompt = f"""
You are a sales representative.

Write a short cold outreach email TO the following prospect:

Prospect name: {lead['name']}
Prospect company: {lead['company']}

Do NOT pretend to be the prospect.
Keep it concise and professional.
Include a subject line.
"""


    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=200,
    )

    return {
        "email": chat.choices[0].message.content
    }
