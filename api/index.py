from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# CORS (permite llamadas desde frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta base opcional (útil para probar rápido)
@app.get("/")
def root():
    return {"message": "API running"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.utcnow()}

# Obtener leads
@app.get("/leads")
def leads():
    return [{"id": 1, "name": "test"}]

# Generar primer email
@app.post("/generate/first/{lead_id}")
def gen(lead_id: int):
    return {"lead_id": lead_id, "email": "ok"}
