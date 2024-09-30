import pandas as pd
import crud, models, schemas
import joblib

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"IA 🦁 Mauvaises Nouvelles 🦁"}

@app.get("/constructors/", response_model=schemas.Constructors)
def read_constructors(db: Session = Depends(get_db)):
    constructors = crud.get_constructors(db)
    return {"constructors": constructors}

@app.post("/constructor/", response_model=schemas.Constructor)
def create_constructor(constructor: schemas.CreateConstructor, db: Session = Depends(get_db)):
    return crud.set_constructor(db, constructor)

@app.get("/circuits/", response_model=schemas.Circuits)
def read_circuits(db: Session = Depends(get_db)):
    circuits = crud.get_circuits(db)
    return {"circuits": circuits}

@app.post("/circuit/", response_model=schemas.Circuit)
def create_circuit(circuit: schemas.CreateCircuit, db: Session = Depends(get_db)):
    return crud.set_circuit(db, circuit)

@app.post("/predict/", response_model=schemas.Predict)
def create_predict(predict: schemas.CreatePredict, db: Session = Depends(get_db)):
    # Chargement des modèles et des encoders
    rf_model = joblib.load('xgboost_model.pkl')
    label_encoder_circuit = joblib.load('label_encoder_circuit.pkl')
    label_encoder_constructor = joblib.load('label_encoder_constructor.pkl')
    label_encoder_year = joblib.load('label_encoder_year.pkl')

    # Nouvelle entrée
    new_data = {
        'grid': 5,
        'circuitRef': 'bahrain',
        'constructorRef': 'red_bull',
        'year': 2024
    }

    # Transformer les strings en catégories avec les encoders
    new_data['circuitRef'] = label_encoder_circuit.transform([new_data['circuitRef']])[0]
    new_data['constructorRef'] = label_encoder_constructor.transform([new_data['constructorRef']])[0]
    new_data['year'] = label_encoder_year.transform([new_data['year']])[0]

    # Créer un DataFrame pour la prédiction
    new_data_df = pd.DataFrame([new_data])

    # Prédire la position finale
    predicted_position = rf_model.predict(new_data_df)
    print(f"Position finale prédite : {predicted_position[0].round(0)}")
    return {"predict": predict}