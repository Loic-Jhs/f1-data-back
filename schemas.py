from pydantic import BaseModel
from typing import List


class CreateConstructor(BaseModel):
    name: str
    ref: str


class Constructor(CreateConstructor):
    id: int

    class Config:
        orm_mode = True


class Constructors(BaseModel):
    constructors: List[Constructor]


class CreateCircuit(BaseModel):
    name: str
    ref: str


class Circuit(CreateCircuit):
    id: int

    class Config:
        orm_mode = True


class Circuits(BaseModel):
    circuits: List[Circuit]


class CreatePredict(BaseModel):
    grid: str
    circuit: str
    constructor: str
    year: str


class Predict(CreatePredict):
    id: int
    predicted_position: int

    class Config:
        orm_mode = True
