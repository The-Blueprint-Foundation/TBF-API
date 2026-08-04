from fastapi import FastAPI

app = FastAPI(title="FastAPI on GCP")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Hello from FastAPI on Google Cloud!"}