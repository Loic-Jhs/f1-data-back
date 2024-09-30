import pandas as pd
import joblib
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Configuration CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes API
@app.get("/")
def read_root():
    return {"message": "IA 🦁 Mauvaises Nouvelles 🦁"}

@app.get("/constructors/", response_model=schemas.Constructors)
def read_constructors(db: Session = Depends(_get_db)):
    return {"constructors": crud.fetch_all_constructors(db)}

@app.post("/constructor/", response_model=schemas.Constructor)
def create_constructor(constructor: schemas.CreateConstructor, db: Session = Depends(_get_db)):
    return crud.add_constructor(db, constructor)

@app.get("/circuits/", response_model=schemas.Circuits)
def read_circuits(db: Session = Depends(_get_db)):
    return {"circuits": crud.fetch_all_circuits(db)}

@app.post("/circuit/", response_model=schemas.Circuit)
def create_circuit(circuit: schemas.CreateCircuit, db: Session = Depends(_get_db)):
    return crud.add_circuit(db, circuit)

@app.post("/predict/", response_model=schemas.Predict)
def predict_race(predict: schemas.CreatePredict, db: Session = Depends(_get_db)):
    return crud.process_race_prediction(db, predict)
