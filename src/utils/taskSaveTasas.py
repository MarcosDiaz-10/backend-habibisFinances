

import asyncio
import asyncpg
from scrapper.service import getBcvTasa,  getBinanceTasaV2


async def taskSaveTasas(time: int, pool: asyncpg.Pool):
    """
    Funcion para guardar las tasas en la base de datos cada cierto tiempo.
    """
    while True:
       tasaBCV = getBcvTasa() 
       tasaParalelo = getBinanceTasaV2()
       if not tasaBCV["error"] and not tasaParalelo["error"]:
          async with pool.acquire() as conn:
            await conn.execute("INSERT INTO finances.historial_tasas (id_tipo_tasa, fecha,valor_tasa) VALUES (1, NOW(), $1);", float(tasaBCV["price"].replace(",", ".")))
            await conn.execute("INSERT INTO finances.historial_tasas (id_tipo_tasa, fecha,valor_tasa) VALUES (2, NOW(), $1);", float(tasaParalelo["price"].replace(",", ".")))
       await asyncio.sleep(time) 
