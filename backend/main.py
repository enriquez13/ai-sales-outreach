from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Lead
import csv
from hf_client import generate_email
from datetime import datetime, timedelta

app = FastAPI()
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    yield db
    db.close()

@app.post("/upload")
async def upload(file:UploadFile, db:Session=Depends(get_db)):

    content = await file.read()
    rows = csv.DictReader(content.decode().splitlines())

    for r in rows:
        db.add(Lead(**r))

    db.commit()

@app.get("/leads")
def leads(db:Session=Depends(get_db)):
    return db.query(Lead).all()

@app.post("/generate/{lead_id}")
def gen(lead_id:int, db:Session=Depends(get_db)):

    lead = db.get(Lead, lead_id)
    email = generate_email(lead)

    return {"email":email}

@app.get("/followups")
def followups(db:Session=Depends(get_db)):

    limit = datetime.utcnow()-timedelta(days=10)

    return db.query(Lead).filter(
        Lead.status=="first_sent",
        Lead.first_email_date < limit
    ).all()
