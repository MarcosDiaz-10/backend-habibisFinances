

from pydantic import BaseModel, EmailStr

# Respuesta que se le da al hacer login
class ResponseLogin(BaseModel):
    error: bool
    access_token: str
    refresh_token: str
   

class RequestUserLogin(BaseModel):
    email: EmailStr 
    password: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str