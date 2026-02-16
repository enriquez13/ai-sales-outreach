from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow()}

@app.get("/leads")
def leads():
    return [{"id": 1, "name": "test"}]

@app.post("/generate/first/{lead_id}")
def gen(lead_id: int):
    return {"lead_id": lead_id, "email": "ok"}


handler = app
