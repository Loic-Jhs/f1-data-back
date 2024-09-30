from copyreg import constructor
from pydantic import BaseModel
from typing import List

class CreateConstructor(BaseModel):
    name: str

class Constructor(CreateConstructor):
    id: int
    
    class Config:
        orm_mode = True

class Constructors(BaseModel):
    constructors: list[Constructor]

class CreateCircuit(BaseModel):
    name: str

class Circuit(CreateCircuit):
    id: int

    class Config:
        orm_mode = True

class Circuits(BaseModel):
    circuits: list[Circuit]

class CreatePredict(BaseModel): 
    grid: str
    circuit: str
    constructor: str
    year: str

class Predict(CreatePredict):
    id: int
    class Config:
        orm_mode = True

