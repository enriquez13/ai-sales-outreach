from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from groq import Groq
import os

# Configuración DB
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== ENDPOINTS ==========

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API funcionando en Railway!"}

@app.get("/leads")
def get_leads(db: Session = Depends(get_db)):
    db_leads = db.query(Lead).all()
    results = []
    for lead in db_leads:
        l_data = {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "company": lead.company,
            "stage": lead.stage,
            "sent_at": lead.sent_at.isoformat() if lead.sent_at else None,
            "sent_time": lead.sent_at.strftime("%H:%M") if lead.sent_at else None,
            "days_left": 5
        }
        if lead.stage == "followup" and lead.sent_at:
            diferencia = datetime.now() - lead.sent_at
            l_data["days_left"] = max(0, 5 - diferencia.days)
        results.append(l_data)
    return results

@app.post("/generate/first/{lead_id}")
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

@app.patch("/leads/{lead_id}/complete")
def complete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    
    if lead.stage == "new":
        lead.stage = "followup"
    elif lead.stage == "followup":
        lead.stage = "negotiation"
    
    lead.sent_at = datetime.now()
    db.commit()
    db.refresh(lead)
    
    return {
        "message": "Progresso atualizado",
        "lead": {
            "id": lead.id,
            "stage": lead.stage,
            "sent_at": lead.sent_at.isoformat()
        }
    }

@app.patch("/leads/{lead_id}/negotiation")
def move_to_negotiation(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    
    lead.stage = "negotiation"
    db.commit()
    return {"message": "Lead movido a negociación"}