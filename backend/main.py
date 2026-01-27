from fastapi import FastAPI, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Lead
import csv
from hf_client import generate_email
from datetime import datetime, timedelta

app = FastAPI()

# Configuración de CORS: Permite que tu URL de Vercel acceda a los datos
origins = [
    "https://ai-sales-outreach-sandy.vercel.app",
    "http://localhost:5173", # Para pruebas locales con Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

@app.on_event("startup")
def startup_populate():
    db = SessionLocal()
    # Solo crea el lead si la tabla está vacía
    if db.query(Lead).count() == 0:
        test_lead = Lead(
            name="Juan Perez", 
            email="juan@ejemplo.com", 
            company="Empresa Test", 
            category="Tecnología",
            status="new"
        )
        db.add(test_lead)
        db.commit()
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload(file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()
    rows = csv.DictReader(content.decode().splitlines())
    for r in rows:
        db.add(Lead(**r))
    db.commit()
    return {"status": "success"}

@app.get("/leads")
def leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()

@app.post("/generate/{lead_id}")
def gen(lead_id: int, db: Session = Depends(get_db)):
    # 1. Buscamos el lead en la base de datos
    lead = db.get(Lead, lead_id)
    if not lead:
        return {"error": "Lead no encontrado"}
    
    # 2. Llamamos a tu función de Hugging Face
    email_content = generate_email(lead)
    
    # 3. CÓDIGO NUEVO:
    # Actualizamos el estado para que el sistema sepa que ya se envió el primero
    lead.status = "first_sent" 
    # Guardamos la fecha y hora exacta de hoy
    lead.first_email_date = datetime.utcnow() 
    
    # 4. Guardamos los cambios en la base de datos
    db.commit()
    
    return {"email": email_content}

@app.get("/followups")
def followups(db: Session = Depends(get_db)):
    limit = datetime.utcnow() - timedelta(days=5)
    return db.query(Lead).filter(
        Lead.status == "first_sent",
        Lead.first_email_date < limit
    ).all()