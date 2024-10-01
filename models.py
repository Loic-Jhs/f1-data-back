from weakref import ref
from sqlalchemy import Column, Integer, String
from database import Base


class Constructors(Base):
    __tablename__ = "constructors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)


class Circuit(Base):
    __tablename__ = "circuits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Predict(Base):
    __tablename__ = "predicts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    grid = Column(Integer, nullable=False)
    circuit = Column(String, nullable=False)
    constructor = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    predicted_position = Column(Integer, nullable=False)
