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
Escreva um PRIMEIRO email de contato para {lead['name']} da empresa {lead['company']}.

ESTRUTURA OBRIGATÓRIA (Siga exatamente esta ordem):
1. Saudação: "Olá {lead['name']}, boa tarde! Tudo bem?"
2. Pergunta de gancho: "você já teve contato com a Delfia?"
3. Declaração de autoridade: "Como **pioneira e líder**:"
4. Lista de benefícios (Use exatamente estes 3 bullets com as negritas indicadas):
   • Entregamos significativo impacto nos custos através das soluções **Grafana**;
   • Utilizamos a **CRIBL** para reduzir e rotear dados de TI e segurança de qualquer fonte para qualquer destino reduzindo gastos em até 60%;
   • Apoiamos e complementamos projetos já existentes com **capacidade técnica** diferenciada.

5. Call to Action: "Vamos trazer esses ganhos para a {lead['company']}?"

6. Assinatura:
Grato,
**Felipe Ommundsen**
Enterprise Sales
Delfia

REGRAS DE FORMATAÇÃO:
- Use bullets (•) e não hifens.
- Respeite as negritas (**) conforme o modelo.
- NÃO adicione texto extra, introduções ou conclusões além do solicitado.
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
Escreva um email de FOLLOW-UP (após 5 dias) para {lead['name']} da empresa {lead['company']}.

ESTRUTURA OBRIGATÓRIA (Siga exatamente esta ordem):
1. Saudação: "Olá {lead['name']}, tudo bem?"
2. Pergunta de gancho: "Seria má idéia ter a **Delfia** como referência de melhores práticas em **observabilidade**?"
3. Contexto: "Pelo que pesquisei, os temas abaixo poderiam interessar a {lead['company']}:"
4. Lista técnica (Use exatamente estes 6 bullets):
   • Observabilidade container (Prometheus, Grafana, Elastic Stack)
   • APM (Application Performance Monitoring) para SAP S/4HANA
   • Log aggregation centralizado
   • Distributed tracing para microserviços
   • Dashboards operacionais em tempo real
   • Alertas preditivos com ML

5. Call to Action: "Vamos trazer esses ganhos para a {lead['company']}?"

6. Assinatura:
Grato,
**Felipe Ommundsen**
Enterprise Sales
Delfia

REGRAS DE FORMATAÇÃO:
- Use bullets (•) exatamente como no modelo.
- NÃO invente introduções.
- Mantenha as negritas (**) em Delfia, observabilidade e no nome da assinatura.
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=250,
    )

    return {"email": chat.choices[0].message.content}
