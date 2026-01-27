import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS ultra-permisiva para evitar bloqueos con Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos de ejemplo
leads = [
    {"id": 1, "name": "Juan Perez", "company": "Empresa Test", "category": "Tecnología", "status": "new"}
]

@app.get("/leads")
async def get_leads():
    return leads

@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):
    # 1. Buscar el lead
    lead = next((l for l in leads if l.id == lead_id), None)
    if not lead:
        return {"email": "❌ Error: Lead no encontrado en la base de datos."}

    # 2. Verificar Token
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        return {"email": "⚠️ Error: HF_TOKEN no detectado. Revisa 'Environment' en Render."}

    # 3. Configurar llamada a Hugging Face
    # Usaremos Mistral que es más confiable para textos cortos
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {api_token}"}
    prompt = f"Write a professional 2-sentence sales email for {lead['name']} from {lead['company']}."
    
    try:
        response = requests.post(api_url, headers=headers, json={"inputs": prompt}, timeout=15)
        
        # Si Hugging Face está cargando el modelo (Error 503)
        if response.status_code == 503:
            return {"email": "⏳ La IA se está activando. Por favor, reintenta en 15 segundos."}
            
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return {"email": result[0].get('generated_text', "No se pudo generar el texto.")}
        else:
            return {"email": f"❌ Error de IA: {result.get('error', 'Respuesta inesperada')}"}

    except Exception as e:
        return {"email": f"🚀 Error de conexión: {str(e)}"}