from datetime import datetime, timezone
from re import I
from typing import Annotated
from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException

from auth.models import RequestUserLogin, ResponseLogin, TokenRefreshRequest
from auth.services import createAccessToken, createRefreshToken
from constants import RESPONSE_BAD_REQUEST
from dependencies import getDbConnection
from users.services import authenticateUser, getUserById


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses=RESPONSE_BAD_REQUEST,
)


@router.post('/login', response_model=ResponseLogin)
async def login(userLogin: RequestUserLogin, conn: Annotated[Connection, Depends(getDbConnection)]):
    """
    Endpoint para obtener un token de acceso
    """
    user = await authenticateUser(userLogin.email, userLogin.password, conn)
    if user['error'] or not user['data']:
       raise HTTPException(status_code=400, detail=user) 

    userObject = user["data"]
    access_token = createAccessToken(data={"sub": userObject.id, "email": userObject.email, "nombre": userObject.nombre, "apellido": userObject.apellido})
    refresh_token = await createRefreshToken(data={"sub": userObject.id,  "nombre": userObject.nombre, "apellido": userObject.apellido}, conn=conn)
    return {
        "error": False,
        "access_token": access_token,
        "refresh_token": refresh_token if refresh_token else "",
        
    }
@router.post('/refresh', response_model=ResponseLogin)
async def refresh_token(refreshRequest: TokenRefreshRequest, conn: Annotated[Connection, Depends(getDbConnection)]):
    """
    Endpoint para refrescar el token de acceso
    """
    token = refreshRequest.refresh_token

    try:
        tokenDB = await conn.fetchrow(
            "SELECT * FROM finances.refresh_tokens WHERE token = $1", token)
        if not tokenDB:
            raise HTTPException(status_code=400, detail={
                "error": True, "msg": "Token de refresco no encontrado"
            }) 
        
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "error": True, "msg": "Error al buscar el token de refresco"
        })
        
    if tokenDB['expires_at'] <  datetime.now(timezone.utc).replace(tzinfo=None):
        await conn.execute("DELETE FROM finances.refresh_tokens WHERE token = $1", token)
        raise HTTPException(status_code=401, detail={
            "error": True, "msg": "Token de refresco expirado"
        })

    returnUser = await getUserById(tokenDB['id_user'], conn)
    if not returnUser or returnUser['error']:
        raise HTTPException(status_code=401, detail={"error": True, "msg": "Usuario no encontrado"})
    user = returnUser['data']
    
    try:
        await conn.execute("DELETE FROM finances.refresh_tokens WHERE token = $1", token)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "msg": f"Error al generar los tokens: {e}"})
    
    new_access_token = createAccessToken(data={"sub": user.id, "email": user.email, "nombre": user.nombre, "apellido": user.apellido})
    new_refresh_token = await createRefreshToken(data={"sub": user.id, "nombre": user.nombre, "apellido": user.apellido}, conn=conn)
    
    return {
        "error": False,
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        
    }
    