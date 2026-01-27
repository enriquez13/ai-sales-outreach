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

# LEADS
leads = [
    {
        "id": 1,
        "name": "Allan",
        "company": "Hypera",
        "stage": "new"
    },
    {
        "id": 2,
        "name": "Maria Gonzalez",
        "company": "Tech Solutions",
        "stage": "new"
    },
    {
        "id": 3,
        "name": "Sara Rubio",
        "company": "TechCorp",
        "stage": "followup"
    }
]

@app.get("/leads")
def get_leads():
    return leads


# PRIMER EMAIL
@app.post("/generate/first/{lead_id}")
def first_email(lead_id: int):

    lead = next((l for l in leads if l["id"] == lead_id), None)

    if not lead:
        return {"email": "Lead no encontrado"}

    prompt = f"""
Você é Felipe Ommundsen, Enterprise Sales da Delfia.

Escreva um PRIMEIRO email de contato em português:

Assunto: {lead['company']} & Delfia (Observabilidade)

Inclua:

- saudação
- pergunta inicial
- Grafana
- Cribl
- redução de custos
- convite final

Prospecto:
{lead['name']} – {lead['company']}
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=250,
    )

    return {"email": chat.choices[0].message.content}


# FOLLOW UP
@app.post("/generate/followup/{lead_id}")
def followup_email(lead_id: int):

    lead = next((l for l in leads if l["id"] == lead_id), None)

    if not lead:
        return {"email": "Lead no encontrado"}

    prompt = f"""
Segundo email de follow-up após 5 dias.

Inclua:

Observabilidade container  
APM SAP  
Logs centralizados  
Tracing distribuído  
Dashboards em tempo real  
Alertas ML  

Finalize convidando novamente.

Prospecto:
{lead['name']} – {lead['company']}
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=250,
    )

    return {"email": chat.choices[0].message.content}
