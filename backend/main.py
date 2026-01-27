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
    lead = db.get(Lead, lead_id)
    email = generate_email(lead)
    return {"email": email}

@app.get("/followups")
def followups(db: Session = Depends(get_db)):
    limit = datetime.utcnow() - timedelta(days=10)
    return db.query(Lead).filter(
        Lead.status == "first_sent",
        Lead.first_email_date < limit
    ).all()