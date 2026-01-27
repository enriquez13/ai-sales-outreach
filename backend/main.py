import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

leads_db = [{"id": 1, "name": "Juan Perez", "company": "Empresa Test"}]

@app.get("/leads")
async def get_leads():
    return leads_db

@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):
    token = os.getenv("HF_TOKEN")
    lead = next((l for l in leads_db if l.id == lead_id), None)

    if not token: return {"email": "❌ Error: Configura el HF_TOKEN en Render."}
    if not lead: return {"email": "❌ Error: Cliente no encontrado."}

    # URL para Mistral-7B-Instruct-v0.3
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Formato de chat recomendado para modelos Instruct
    payload = {
        "inputs": f"[INST] Write a professional 2-line sales email for {lead['name']} from {lead['company']}. [/INST]",
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7 # Añadimos un poco de creatividad
        }
    }

    try:
        # Aumentamos el timeout porque v0.3 es un modelo más denso
        response = requests.post(api_url, headers=headers, json=payload, timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            # Acceder al texto generado
            return {"email": result[0].get('generated_text', "No se generó contenido.")}
        
        if response.status_code == 503:
            return {"email": "⏳ El modelo v0.3 se está cargando. Reintenta en 20 segundos."}
            
        return {"email": f"Error {response.status_code}: {response.text[:100]}"}

    except Exception as e:
        # Esto atrapa errores de red y evita el Error 500 de FastAPI
        return {"email": f"Error de conexión: {str(e)}"}