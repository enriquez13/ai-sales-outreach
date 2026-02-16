from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
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

# ✅ CORRECCIÓN: Sin /api/ en las rutas
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

# Handler para Vercel
handler = app