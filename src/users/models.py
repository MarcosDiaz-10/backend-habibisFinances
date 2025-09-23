from datetime import date
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono: str

class UserToken(BaseModel):
    id: str
    email: EmailStr
    nombre: str
    apellido: str