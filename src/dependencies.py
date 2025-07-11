from fastapi import Request, HTTPException

import asyncpg

async def getDbConnection(request: Request):
    """
    Dependencia que obtiene una conexión del pool y la devuelve al final.
    """
    # El pool fue almacenado en el estado de la app durante el inicio
    pool = request.app.state.dbPool
    # 'acquire' toma una conexión del pool
    async with pool.acquire() as connection:
        # El bloque 'async with' se asegura de que la conexión
        # se devuelva ('release') al pool automáticamente al salir del bloque,
        # ya sea de forma normal o por una excepción.
        try:
            yield connection
        except asyncpg.PostgresError as e:
            # Manejo de errores específicos de la base de datos si es necesario
            # Por ejemplo, registrar el error
            raise HTTPException(status_code=500, detail=f"Database error: {e}")