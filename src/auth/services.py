from datetime import datetime, timezone, timedelta
from typing import Annotated
from asyncpg import Connection
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from config import getSettings
from dependencies import getDbConnection

settings = getSettings()
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
    """Verifica Si la contrasenia que se toma es al misma que esta hasheada"""
    return pwdContext.verify(plainPassword, hashedPassword)

def getPasswordHash(password: str) -> str:
    """Hashea la contrasenia que se le pasa por parametro"""
    return pwdContext.hash(password)

def createAccessToken(data: dict) -> str:
    """Crea el token de acceso JWT"""
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})
    encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM_TOKEN)
    return encodedJwt


def createRefreshToken(data: dict) -> str:
    """Crea el token de refresco JWT"""
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    toEncode.update({"exp": expire})
    encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM_TOKEN)
    return encodedJwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def getCurrentUser(
    token: Annotated[str, Depends(oauth2_scheme)],
    conn: Annotated[Connection, Depends(getDbConnection)]
):
    """Obtiene el usuario a partir del token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM_TOKEN])
        userId = payload.get("sub")
        if  userId is None:
            raise credentials_exception
    
    except JWTError:
        raise credentials_exception
   
    user = conn.fetchrow("SELECT * FROM finances.usuarios WHERE id_user = $1", int(userId))

    if user is None:
        raise credentials_exception

    return user