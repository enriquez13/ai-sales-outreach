import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Configuración de CORS para que Vercel pueda hablar con Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos de prueba
leads = [
    {"id": 1, "name": "Juan Perez", "company": "Empresa Test", "category": "Tecnología", "status": "new"}
]

HF_TOKEN = os.getenv("HF_TOKEN")
# Usaremos un modelo más ligero y rápido para evitar el timeout de Render
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

@app.get("/leads")
async def get_leads():
    return leads

@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):
    lead = next((l for l in leads if l.id == lead_id), None)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")

    if not HF_TOKEN:
        return {"email": "⚠️ Error: HF_TOKEN no configurado en Render."}

    prompt = f"Write a short professional sales email for {lead['name']} from {lead['company']}. Category: {lead['category']}."
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        result = response.json()
        
        # Hugging Face a veces devuelve una lista o un error de 'loading'
        if isinstance(result, list):
            return {"email": result[0]['generated_text']}
        elif "estimated_time" in result:
            return {"email": "⏳ El modelo de IA se está cargando. Reintenta en 20 segundos."}
        else:
            return {"email": f"❌ Error de la IA: {result.get('error', 'Desconocido')}"}
            
    except Exception as e:
        return {"email": f"❌ Error de conexión: {str(e)}"}