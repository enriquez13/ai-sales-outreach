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
        "email": "jhoneriquez@unicauca.edu.co",
        "company": "Hypera",
        "stage": "new"
    },
    {
        "id": 2,
        "name": "Maria Gonzalez",
        "email": "jhoneriquez@unicauca.edu.co",
        "company": "Tech Solutions",
        "stage": "new"
    },
    {
        "id": 3,
        "name": "Sara Rubio",
        "email": "jhoneriquez@unicauca.edu.co",
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

Escreva um PRIMEIRO email de contato (cold email) em português.

Objetivo: iniciar conversa, não vender.

REGRAS OBRIGATÓRIAS:
- NÃO assuma relacionamento prévio
- NÃO diga que já conversamos
- NÃO escreva email longo
- NÃO use linguagem corporativa genérica
- Tom humano, direto e profissional

Assunto: {lead['company']} & Delfia (Observabilidade)

Corpo:

1. Cumprimento curto usando {lead['name']}
2. Frase direta explicando o motivo do contato
3. Uma pergunta aberta relacionada a desafios técnicos
4. 2–3 bullets com exemplos de valor
5. Pergunta final simples

Temas permitidos:
- Observabilidade de aplicações
- Monitoramento SAP S/4HANA
- Logs centralizados
- Alertas inteligentes
- Performance de containers

Finalize com:

"Faz sentido conversarmos por 15 minutos?"
Assinatura:
Felipe Ommundsen  
Enterprise Sales
Delfia 

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
Você é Felipe Ommundsen, Enterprise Sales da Delfia.

Escreva um email de follow-up (após 5 dias) em português.

REGRAS OBRIGATÓRIAS:
- NÃO diga que houve conversa anterior
- NÃO diga “seguindo nossa conversa”
- NÃO assuma contato prévio
- NÃO escreva email longo
- Seja direto, comercial e objetivo

Estrutura OBRIGATÓRIA:

Assunto: {lead['company']} & Delfia (Observabilidade)

Corpo:
- Cumprimento curto
- Pergunta retórica simples
- Lista curta de temas relevantes (bullet points)
- Convite final curto

Inclua APENAS estes temas:
- Observabilidade container (Prometheus, Grafana, Elastic Stack)
- APM para SAP S/4HANA
- Log aggregation centralizado
- Distributed tracing
- Dashboards operacionais
- Alertas preditivos com ML

Finalize com:
"Vamos trazer esses ganhos para a {lead['company']}?"

Assinatura:
Felipe Ommundsen  
Enterprise Sales – Delfia
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=250,
    )

    return {"email": chat.choices[0].message.content}
