import os
from datetime import datetime, timedelta
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
Escreva um PRIMEIRO email de contato para {lead['name']} da empresa {lead['company']}.

ESTRUTURA OBRIGATÓRIA:
1. Saudação: "Olá {lead['name']}, boa tarde! Tudo bem?"
2. "você já teve contato com a Delfia?"
3. "Como pioneira e líder em soluções de monitoramento de processos e análise de dados, a Delfia oferece:"
4. Lista (Use bullets •):
   • Entregamos significativo impacto nos custos através das soluções Grafana;
   • Utilizamos a CRIBL para reduzir e rotear dados de TI e segurança de qualquer fonte para qualquer destino reduzindo gastos em até 60%;
   • Apoiamos e complementamos projetos já existentes com capacidade técnica diferenciada.

5. "Vamos trazer esses ganhos para a {lead['company']}?"

6. Assinatura:
Grato,
Felipe Ommundsen
Enterprise Sales
Delfia

REGRA CRÍTICA: NÃO use asteriscos (**) nem Markdown. Use apenas texto puro.
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
Escreva um email de FOLLOW-UP para {lead['name']} da empresa {lead['company']}.

ESTRUTURA OBRIGATÓRIA:
1. Saudação: "Olá {lead['name']}, tudo bem?"
2. "Seria má idéia ter a Delfia como referência de melhores práticas em observabilidade?"
3. "Pelo que pesquisei, os temas abaixo poderiam interessar a {lead['company']}:"
4. Lista técnica (bullets •):
   • Observabilidade container (Prometheus, Grafana, Elastic Stack)
   • APM para SAP S/4HANA
   • Log aggregation centralizado
   • Distributed tracing para microserviços
   • Dashboards operacionais em tempo real
   • Alertas preditivos com ML

5. "Vamos trazer esses ganhos para a {lead['company']}?"

6. Assinatura:
Grato,
Felipe Ommundsen
Enterprise Sales
Delfia

REGRA CRÍTICA: NÃO use asteriscos (**) nem Markdown. Use apenas texto puro.
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=250,
    )

    return {"email": chat.choices[0].message.content}

# Endpoint para actualizar el estado del lead
@app.patch("/leads/{lead_id}/complete")
def complete_lead(lead_id: int):
    lead = next((l for l in leads if l["id"] == lead_id), None)
    if not lead:
        return {"error": "Lead no encontrado"}
    
    # Cambiamos el estado y guardamos la metadata
    lead["stage"] = "followup"
    lead["sent_at"] = datetime.now().isoformat() # Convertimos a texto para evitar errores de JSON
    lead["days_left"] = 5 
    
    return {"message": "Lead actualizado", "lead": lead}