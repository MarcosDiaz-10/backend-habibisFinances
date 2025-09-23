

from typing import TypedDict
from asyncpg import Connection

from auth.services import getPasswordHash, verifyPassword
from users.models import UserCreate, UserInDB

class ResposeGetUser(TypedDict):
    data: UserInDB | None
    msg: str
    error: bool

async def getUserById(userId: str, conn: Connection) -> ResposeGetUser:
    """Busca un usuario por su ID"""
    try:
        print(userId)
        query= """
            SELECT id_user as id, nombre, apellido, correo as email, password_user as password, fecha_nacimiento, telefono
            FROM finances.usuarios WHERE id_user=$1;
        """
        user = await conn.fetchrow(query, userId)
        if not user:
            return {
                "data": None,
                "msg": "Usuario no encontrado",
                "error": True
            } 
        return {
            "data": UserInDB(**user),
            "msg": "",
            "error": False
        }
    except Exception as e:
        return {
            "data": None,
            "msg": f"Error al buscar el usuario: {e} ",
            "error": True
        }

async def getUserByEmail(email: str, conn: Connection) -> ResposeGetUser:
    """Busca un usuario por su email"""
    try:
        query = """
        SELECT id_user as id, nombre, apellido, correo as email, password_user as password, fecha_nacimiento, telefono FROM finances.usuarios WHERE correo=$1;
        """
        userSearch = await conn.fetchrow(query, email)
        user = dict(userSearch) if userSearch else None
        if not user:
            return {
                "data": None,
                "msg": "Usuario no encontrado",
                "error": True
            }
        return {
            "data": UserInDB(**user) ,
            "msg": "",
            "error": False
        }
    except Exception as e:
        return {
            "data": None,
            "msg": f"Error al buscar el usuario: {e} ",
            "error": True
        }


async def createUser(user: UserCreate, conn: Connection):
    """Crea un nuevo usuario en la base de datos"""
    passwordHash = getPasswordHash(user.password)
    try:
        await conn.execute(
        "INSERT INTO finances.usuarios (correo, password_user, nombre, apellido, fecha_nacimiento, telefono) VALUES ($1, $2, $3, $4, $5, $6);",
        user.email,
        passwordHash,
        user.nombre,
        user.apellido,
        user.fecha_nacimiento,
        user.telefono,
    )
        return {"msg": "Usuario creado exitosamente", "error": False}
    except Exception as e:
        return {
            "msg": f"Error al crear el usuario: {e} ",
            "error": True
        }


async def authenticateUser(email: str, password: str, conn: Connection) -> ResposeGetUser:
    """Autentica un usuario por su email y contrasenia"""

    user = await getUserByEmail(email, conn)
    if user["error"] or user["data"] is None:
        return {"msg": f"Usuario o contrasenia incorrectos no encontro user: {user['msg']} ", "error": True, "data": None}
    
    if not verifyPassword(password, user["data"].password):
        return {"msg": "Usuario o contrasenia incorrectos no era password", "error": True, "data": None}
    
    return {"msg": "", "error": False, "data": user["data"]}



    