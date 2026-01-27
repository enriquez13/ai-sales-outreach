import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS para permitir que Vercel se conecte sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos local para la prueba
leads_db = [
    {"id": 1, "name": "Juan Perez", "company": "Empresa Test", "category": "Tecnología"}
]

@app.get("/leads")
async def get_leads():
    return leads_db

@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):
    # 1. Buscar el lead
    lead = next((l for l in leads_db if l.id == lead_id), None)
    if not lead:
        return {"email": "❌ Lead no encontrado."}

    # 2. Obtener el Token de las variables de entorno de Render
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        return {"email": "⚠️ Error: No se encontró el HF_TOKEN en Render."}

    # 3. Configurar la llamada a la IA (Mistral)
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"inputs": f"Write a professional sales email for {lead['name']} from {lead['company']}. Be concise."}

    try:
        # Petición a Hugging Face
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        
        # Si la IA está cargando (Error 503)
        if response.status_code == 503:
            return {"email": "⏳ La IA se está activando. Reintenta en 15 segundos."}
        
        result = response.json()
        
        # Procesar respuesta exitosa
        if isinstance(result, list) and len(result) > 0:
            return {"email": result[0].get('generated_text', "No se pudo generar el texto.")}
        else:
            return {"email": f"❌ Error de la IA: {str(result)}"}

    except Exception as e:
        return {"email": f"🚀 Error de conexión: {str(e)}"}