from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "API funcionando!"}

@app.get("/api/leads")  
def get_leads():
    return [{"id": 1, "name": "Test", "company": "Test Corp"}]

# ✅ Handler con Mangum (requerido para Vercel)
handler = Mangum(app, lifespan="off")