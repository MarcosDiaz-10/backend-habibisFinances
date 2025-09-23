from fastapi import APIRouter, Depends
from asyncpg.connection import Connection
from dependencies import getDbConnection
from src.constants import respose_bad_request
from scrapper.service import getBcvTasa, getBinanceTasa, getBinanceTasaV2

router = APIRouter(
    prefix="/scrapper",
    tags=["scrapper"],
    responses=respose_bad_request,
)


@router.get("/bcv")
async def get_bcv(conn: Connection = Depends(getDbConnection)):
    """
    Endpoint to get the BCV data.
    """
    # tiposDeTasa = await conn.fetch("Select * from finances.tipos_de_tasa;")
    # print(tiposDeTasa[0]["nombre_tasa"])
    databcv = getBcvTasa()
    tasa = float(databcv["price"].replace(",", "."))
    await conn.execute("INSERT INTO finances.historial_tasas (id_tipo_tasa, fecha,valor_tasa) VALUES (1, NOW(), $1);", tasa)
    if databcv["error"]:
        return {"msg": databcv["msg"], "error": True}
    return {
        "msg": "",
        "error": False,
        "data": tasa,
    }


@router.get("/binance")
async def get_binance(conn: Connection = Depends(getDbConnection)):
    """
    Endpoint to get the Binace data.
    """
    dataBinance = getBinanceTasaV2()
    tasa = float(dataBinance["price"].replace(",", "."))
    await conn.execute("INSERT INTO finances.historial_tasas (id_tipo_tasa, fecha,valor_tasa) VALUES (2, NOW(), $1);", tasa)
    if dataBinance["error"]:
        return {"msg": dataBinance["msg"], "error": True}
    return {
        "msg": '',
        "error": False,
        "data":  tasa,
    }
