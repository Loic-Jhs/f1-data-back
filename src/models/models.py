from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base
from models_enum import UserType, MagasinType

from datetime import datetime


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    guid = Column(String(150), unique=True, nullable=False)
    first_name = Column(String(25), nullable=True)
    last_name = Column(String(25), nullable=True)
    email = Column(String(150), nullable=False)
    password = Column(String(255), nullable=False)
    picture_icon = Column(String(25), default="person")
    type = Column(Enum(UserType.admin, UserType.client, UserType.magasin), default=UserType.client)
    sponsor_code = Column(String(25), unique=True, nullable=False)
    is_sponsored = Column(Boolean, default=False)
    id_sponsor = Column(Integer, ForeignKey("user.id"), nullable=True)
    localisation = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    sponsor = relationship("User", foreign_keys=[id_sponsor])
