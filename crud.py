import models, schemas

from sqlalchemy.orm import Session

import logging

def get_constructors(db: Session):
    return db.query(models.Constructors).all()

def set_constructor(db: Session, constructor: schemas.CreateConstructor):
    try:
        db_constructor = models.Constructors(name=constructor.name)
        db.add(db_constructor)
        db.commit()
        db.refresh(db_constructor)
        return db_constructor
    except Exception as e:
        db.rollback()
        logging.error(f"Error setting constructor: {e}")
        return None
    
def get_circuits(db: Session):
    return db.query(models.Circuit).all()

def set_circuit(db: Session, circuit: schemas.CreateCircuit):
    db_circuit = models.Circuit(**circuit.dict())
    db.add(db_circuit)
    db.commit()
    db.refresh(db_circuit)
    return db_circuit