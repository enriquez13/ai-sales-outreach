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

@app.get("/leads")
async def get_leads():
    return [{"id": 1, "name": "Juan Perez"}]

@app.post("/generate/{lead_id}")
async def generate_email(lead_id: int):
    # Esto atrapará el error exacto y lo mostrará en el navegador
    try:
        token = os.getenv("HF_TOKEN", "MISSING_TOKEN")
        
        # Simulación de llamada para ver si la librería requests funciona
        api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {token}"}
        
        # Hacemos la petición
        res = requests.post(api_url, headers=headers, json={"inputs": "test"}, timeout=5)
        
        return {
            "status": "success",
            "debug_info": f"Token: {token[:5]}...",
            "ai_response": res.json()
        }
    except Exception as e:
        # SI ESTO FALLA, VERÁS EL ERROR AQUÍ EN LUGAR DE UN 500
        return {"status": "error", "message": str(e)}