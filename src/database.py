import asyncpg
import asyncio

from config import getSettings

settings = getSettings()
db_pool = None


async def getDbPool():
    """
    Retorna la instancia del pool de conexiones. La crea si no existe.
    """
    try:
        global db_pool
        if db_pool is None:
            db_pool = await asyncpg.create_pool(
                user=settings.USER_DB,
                password=settings.PASSWORD_DB,
                host=settings.HOST_DB,
                port=settings.PORT_DB,
                database=settings.DB_NAME,
                min_size=settings.DB_POOL_MIN_SIZE,
                max_size=settings.DB_POOL_MAX_SIZE,
            )
        return db_pool
    except asyncpg.PostgresError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return


async def closeDbPool():
    """
    Cierra pool de conexiones.
    """
    global db_pool
    if db_pool is not None:
        await db_pool.close()
        db_pool = None
