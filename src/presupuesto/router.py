from asyncpg import Connection
from fastapi import APIRouter, Depends
from dependencies import getDbConnection
from src.constants import respose_bad_request

router = APIRouter(
    prefix="/presupuesto",
    tags=["presupuesto"],
    responses=respose_bad_request,
)


@router.get("/all")
async def get_presupuesto(conn: Connection = Depends(getDbConnection)):
    """
    Endpoint para obtener una lista de todos los presupuestos existentes.
    """
    presupuestos = conn.fetch("SELECT * FROM finances.presupuesto;")
    
    
    return {"msg": "Presupuesto data", "error": False}