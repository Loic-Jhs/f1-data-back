from pydantic import BaseModel
from typing import Optional

# User schemas
class UserBase(BaseModel):
    first_name: str
    last_name: str

class UserCreate(UserBase):
    email: str
    password: str
    sponsor_code: Optional[str] = None
