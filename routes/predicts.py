from fastapi import FastAPI

from main import app


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict")
async def predict(circuit: str, grille: str, constructeur: str):
    output = ""
    return {"message": f"{output}"}
