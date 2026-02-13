from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from groq import Groq
import os

# Misma configuración DB
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    company = Column(String)
    stage = Column(String, default="new")
    sent_at = Column(DateTime, nullable=True)

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("generate/first/{lead_id}")
def first_email(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")

    prompt = f"""
Você é Felipe Ommundsen, Enterprise Sales da Delfia.
Escreva um PRIMEIRO email de contato para {lead.name} da empresa {lead.company}.
ESTRUTURA OBRIGATÓRIA:
1. Saudação: "Olá {lead.name}, boa tarde! Tudo bem?"
2. "você já teve contato com a Delfia?"
3. "Como pioneira e líder em soluções de monitoramento de processos e análise de dados, a Delfia oferece:"
4. Lista (Use bullets •):
   • Entregamos significativo impacto nos custos através de Grafana;
   • Reduzimos gastos em até 60% com CRIBL;
   • Apoiamos projetos com capacidade técnica diferenciada.
5. "Vamos trazer esses ganhos para a {lead.company}?"
Assinatura: Grato, Felipe Ommundsen - Delfia.
REGRA: Texto puro, sem asteriscos.
"""
    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=250,
    )
    return {"email": chat.choices[0].message.content}

@app.post("/generate/followup/{lead_id}")
def followup_email(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")

    prompt = f"""
Você é Felipe Ommundsen, Enterprise Sales da Delfia.
Escreva um email de FOLLOW-UP para {lead.name} da empresa {lead.company}.
ESTRUTURA:
1. "Olá {lead.name}, tudo bem?"
2. "Seria má idéia ter a Delfia como referência em observabilidade?"
3. "Temas: Observabilidade container, APM SAP S/4HANA, Log aggregation, Tracing."
4. "Vamos trazer esses ganhos para a {lead.company}?"
Assinatura: Grato, Felipe Ommundsen - Delfia.
REGRA: Texto puro, sem asteriscos.
"""
    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=250,
    )
    return {"email": chat.choices[0].message.content}
# Handler para Vercel 
handler = app