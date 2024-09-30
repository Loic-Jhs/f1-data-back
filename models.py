from sqlalchemy import Column, String, Integer

from database import Base

class Constructors(Base):
    __tablename__ = "constructors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
