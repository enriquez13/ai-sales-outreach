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

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/leads")
def leads():
    return [{"id":1,"name":"test"}]

@app.post("/generate/first/{lead_id}")
def gen(lead_id:int):
    return {"email": "ok"}
