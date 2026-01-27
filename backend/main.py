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

# LEADS CON ID
leads = [
    {
        "id": 1,
        "name": "Juan Perez",
        "company": "Empresa Test"
    },
    {
        "id": 2,
        "name": "María González",
        "company": "Tech Solutions"
    },
    {
        "id": 3,
        "name": "Carlos Rodríguez",
        "company": "Innovate Corp"
    },
    {
        "id": 4,
        "name": "Ana López",
        "company": "Digital Growth"
    }
]

@app.get("/leads")
async def get_leads():
    return leads


@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):

    lead = next((l for l in leads if l["id"] == lead_id), None)

    if not lead:
        return {"email": "Cliente no encontrado"}

    prompt = f"""
Eres un representante de ventas llamado Alejandro Enríquez, de la compañía Compañía USP.

Escribe un correo corto de contacto inicial (cold outreach) EN ESPAÑOL.

Nombre del prospecto: {lead['name']}
Empresa del prospecto: {lead['company']}

Incluye asunto.
Mantén tono profesional.
Firma como Alejandro Enríquez.
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
