from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

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