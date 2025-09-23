

from asyncpg import Connection

from auth.services import getPasswordHash, verifyPassword


def getUserById(userId: str, conn: Connection):
    """Busca un usuario por su ID"""
    try:
        user = conn.fetchrow("SELECT * FROM finaces.usuario WHERE id=$1;", userId)
        
        return {
            "data": user,
            "msg": "",
            "error": False
        }
    except Exception as e:
        return {
            "data": None,
            "msg": f"Error al buscar el usuario: {e} ",
            "error": True
        }

def getUserByEmail(email: str, conn: Connection):
    """Busca un usuario por su email"""
    try:
        user = conn.fetchrow("SELECT * FROM finaces.usuario WHERE email=$1;", email)
        return {
            "data": user,
            "msg": "",
            "error": False
        }
    except Exception as e:
        return {
            "data": None,
            "msg": f"Error al buscar el usuario: {e} ",
            "error": True
        }


def createUser(user: dict, conn: Connection):
    """Crea un nuevo usuario en la base de datos"""
    passwordHash = getPasswordHash(user["password"])
    try:
        conn.execute(
        "INSERT INTO finances.usuarios (correo, password_user, nombre, apellido, fecha_nacimiento, telefono) VALUES ($1, $2, $3, $4, $5, $6);",
        user["email"],
        passwordHash,
        user["nombre"],
        user["apellido"],
        user["fecha_nacimiento"],
        user["telefono"],
    )
        return {"msg": "Usuario creado exitosamente", "error": False}
    except Exception as e:
        return {
            "msg": f"Error al crear el usuario: {e} ",
            "error": True
        }

def authenticateUser(email: str, password: str, conn: Connection):
    """Autentica un usuario por su email y contrasenia"""

    user = getUserByEmail(email, conn)
    if user["error"] or user["data"] is None:
        return {"msg": "Usuario o contrasenia incorrectos", "error": True, "data": None}
    
    if not verifyPassword(password, user["data"]["password_user"]):
        return {"msg": "Usuario o contrasenia incorrectos", "error": True, "data": None}
    
    return {"msg": "", "error": False, "data": user["data"]}



    