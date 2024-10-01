import joblib
import pandas as pd
import logging
from sqlalchemy.orm import Session
import models
import schemas

xgboost = joblib.load('pkl/xgboost_model.pkl')
gbr = joblib.load('pkl/gb_model.pkl')
linear_regression = joblib.load('pkl/linear_model.pkl')

model_confidences = {
    xgboost: 0.341,
    gbr: 0.334,
    linear_regression:  0.325
}

label_encoder_circuit = joblib.load('pkl/label_encoder_circuit.pkl')
label_encoder_constructor = joblib.load('pkl/label_encoder_constructor.pkl')
label_encoder_year = joblib.load('pkl/label_encoder_year.pkl')


def _commit_transaction(db: Session, instance):
    try:
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
    except Exception as e:
        db.rollback()
        logging.error(f"Database error: {e}")
        return None


def fetch_all_constructors(db: Session):
    return db.query(models.Constructors).all()


def add_constructor(db: Session, constructor: schemas.CreateConstructor):
    db_constructor = models.Constructors(name=constructor.name)
    return _commit_transaction(db, db_constructor)


def fetch_all_circuits(db: Session):
    return db.query(models.Circuit).all()


def add_circuit(db: Session, circuit: schemas.CreateCircuit):
    db_circuit = models.Circuit(name=circuit.name)
    return _commit_transaction(db, db_circuit)


def _prepare_prediction_data(predict: schemas.CreatePredict):
    try:
        return {
            'grid': int(predict.grid),
            'circuitRef': label_encoder_circuit.transform([predict.circuit])[0],
            'constructorRef': label_encoder_constructor.transform([predict.constructor])[0],
            'year': label_encoder_year.transform([int(predict.year)])[0]
        }
    except Exception as e:
        logging.error(f"Error encoding data: {e}")
        raise ValueError("Invalid data for prediction")


def _predict_with_model(model, new_data):
    try:
        new_data_df = pd.DataFrame([new_data])
        predicted_position = model.predict(new_data_df)[0].round(0)
        return int(predicted_position)
    except Exception as e:
        logging.error(f"Prediction error with model {model}: {e}")
        raise RuntimeError("Prediction failed with model")


def _predict_final_position_weighted(new_data):
    weighted_sum = 0
    for model, confidence in model_confidences.items():
        predicted_position = _predict_with_model(model, new_data)
        weighted_sum += predicted_position * confidence

    return int(round(weighted_sum))


def _record_prediction(db: Session, predict: schemas.CreatePredict, predicted_position: int):
    db_predict = models.Predict(
        grid=int(predict.grid),
        circuit=predict.circuit,
        constructor=predict.constructor,
        year=int(predict.year),
        predicted_position=predicted_position
    )
    return _commit_transaction(db, db_predict)


def process_race_prediction(db: Session, predict: schemas.CreatePredict):
    try:
        new_data = _prepare_prediction_data(predict)
        predicted_position = _predict_final_position_weighted(new_data)
        db_predict = _record_prediction(db, predict, predicted_position)

        if db_predict:
            return schemas.Predict(
                grid=predict.grid,
                circuit=predict.circuit,
                constructor=predict.constructor,
                year=predict.year,
                predicted_position=predicted_position,
                id=db_predict.id
            )
        else:
            return None
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return None