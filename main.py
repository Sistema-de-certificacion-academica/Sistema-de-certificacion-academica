from fastapi import FastAPI

app = FastAPI(
    title="UniCert API",
    description="Sistema de Certificación Académica Digital",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "UniCert API funcionando"}