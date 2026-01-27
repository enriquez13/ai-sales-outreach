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

leads_db = [{"id": 1, "name": "Juan Perez", "company": "Empresa Test", "category": "Tecnología"}]

@app.get("/leads")
async def get_leads():
    return leads_db

@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):
    # 1. Verificación del Token (Tu prueba de seguridad)
    token = os.getenv("HF_TOKEN")
    if not token:
        return {"email": "❌ El servidor no encuentra la variable HF_TOKEN en Render."}

    # 2. Buscar al cliente
    lead = next((l for l in leads_db if l.id == lead_id), None)
    if not lead:
        return {"email": "Lead no encontrado."}

    # 3. Llamada a un modelo más rápido (DistilGPT2)
    # Cambié Mistral por este porque responde instantáneamente para pruebas
    api_url = "https://api-inference.huggingface.co/models/distilgpt2"
    headers = {"Authorization": f"Bearer {token}"}
    prompt = f"Write a professional email for {lead['name']} from {lead['company']}:"

    try:
        response = requests.post(api_url, headers=headers, json={"inputs": prompt}, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return {"email": result[0]['generated_text']}
        else:
            # Si el token está mal o el modelo falla, aquí verás el porqué
            return {"email": f"Respuesta de IA ({response.status_code}): {response.text[:100]}"}
            
    except Exception as e:
        return {"email": f"Error de conexión: {str(e)}"}