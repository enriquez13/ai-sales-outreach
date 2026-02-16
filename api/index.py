from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Python": "on Vercel"}

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}