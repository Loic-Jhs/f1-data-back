from pydantic import BaseModel

class CreateConstructor(BaseModel):
    name: str

class Constructor(CreateConstructor):
    id: int
    
    class Config:
        orm_mode = True

class Constructors(BaseModel):
    constructors: list[Constructor]
    