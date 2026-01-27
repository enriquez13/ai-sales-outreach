import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS ultra-permisivo para evitar bloqueos con Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

leads = [
    {"id": 1, "name": "Juan Perez", "company": "Empresa Test", "category": "Tecnología"}
]

@app.get("/leads")
async def get_leads():
    return leads

@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):
    # 1. Buscar el lead manualmente para evitar errores de lógica
    lead = next((l for l in leads if l.id == lead_id), None)
    if not lead:
        return {"email": "Lead no encontrado"}

    # 2. Obtener Token
    token = os.getenv("HF_TOKEN")
    if not token:
        return {"email": "Error: HF_TOKEN no configurado en Render"}

    # 3. Llamada a Hugging Face con manejo de errores manual
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": f"Write a short sales email for {lead['name']}"}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 503:
            return {"email": "⏳ El modelo de IA se está cargando. Reintenta en 20 segundos."}
            
        data = response.json()
        if isinstance(data, list):
            return {"email": data[0].get('generated_text', "No se generó texto.")}
        return {"email": f"Error de la IA: {str(data)}"}
        
    except Exception as e:
        return {"email": f"Error crítico: {str(e)}"}