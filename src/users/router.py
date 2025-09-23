
from typing import Annotated
from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException
from dependencies import getDbConnection
from constants import RESPONSE_BAD_REQUEST
from users.models import ResposeCreate, UserCreate, UserPublic
from users.services import createUser

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses=RESPONSE_BAD_REQUEST,
)

@router.post('/register', response_model=ResposeCreate,status_code=201)
async def registerUser( user: UserCreate, conn: Annotated[Connection, Depends(getDbConnection)]):
    """
    Endpoint para registrar un usuario
    """

    searchUser = await conn.fetchrow("SELECT * FROM finances.usuarios WHERE correo=$1;", user.email)
    existingUser = dict(searchUser) if searchUser else None 
   
    if existingUser:
        raise HTTPException(
            status_code=400,
            detail={"msg": "El usuario ya existe", "error": True}
        ) 

    newUser = await createUser(user, conn) 
    
    if newUser['error']:
        raise HTTPException(
            status_code=400,
            detail={"msg": newUser['msg'], "error": True}
        )
    return newUser    