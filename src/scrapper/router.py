from fastapi import APIRouter, Depends
from asyncpg.connection import Connection
from dependencies import getDbConnection

from scrapper.service import getBcvTasa, getBinanceTasa, getBinanceTasaV2

router = APIRouter(
    prefix="/scrapper",
    tags=["scrapper"],
    responses={404: {"description": "Not found"}},
)


@router.get("/bcv")
async def get_bcv():
    """
    Endpoint to get the BCV data.
    """
    # tiposDeTasa = await conn.fetch("Select * from finances.tipos_de_tasa;")
    # print(tiposDeTasa[0]["nombre_tasa"])
    databcv = getBcvTasa()
    if databcv["error"]:
        return {"msg": databcv["msg"], "error": True}
    return {
        "msg": "",
        "error": False,
        "data": float(databcv["price"].replace(",", ".")),
    }


@router.get("/binance")
def get_binance():
    """
    Endpoint to get the Binace data.
    """
    dataBinance = getBinanceTasaV2()
    if dataBinance["error"]:
        return {"msg": dataBinance["msg"], "error": True}
    return {
        "msg": '',
        "error": False,
        "data":  float(dataBinance["price"].replace(",", ".")),
    }
