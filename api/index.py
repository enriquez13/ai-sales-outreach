from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "API funcionando!"}

@app.get("/api/leads")
def get_leads():
    return [
        {"id": 1, "name": "Test Lead", "company": "Test Corp"}
    ]

handler = app