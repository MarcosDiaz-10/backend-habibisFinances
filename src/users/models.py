from datetime import date
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono: str

class UserPublic(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str

class ResposeCreate(BaseModel):
    msg: str
    error: bool
class UserInDB(UserCreate):
    id: int 
    
    
     
class UserToken(BaseModel):
    id: str
    email: EmailStr
    nombre: str
    apellido: str

