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

@app.get("/api/health")
def health_check():
    return {
        "status": "OK",
        "message": "API funcionando correctamente!",
        "timestamp": datetime.now().isoformat(),
        "vercel": "Python serverless está activo"
    }

@app.get("/api/leads")
def get_fake_leads():
    # Datos falsos sin base de datos
    return [
        {
            "id": 1,
            "name": "María González",
            "email": "maria@test.com",
            "company": "Tech Corp",
            "stage": "new",
            "sent_at": None,
            "days_left": 5
        },
        {
            "id": 2,
            "name": "Carlos Pérez",
            "email": "carlos@test.com",
            "company": "Innovation SA",
            "stage": "followup",
            "sent_at": "2025-02-10T10:30:00",
            "days_left": 3
        }
    ]

@app.post("/api/generate/first/{lead_id}")
def generate_fake_email(lead_id: int):
    # Email fake sin usar Groq
    return {
        "email": f"Olá! Este es un email de prueba generado para el lead {lead_id}. La API funciona correctamente."
    }

# Handler para Vercel
handler = app