from contextlib import asynccontextmanager
from fastapi import FastAPI
from scrapper import router as scrapper
from database import getDbPool, closeDbPool


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.dbPool = await getDbPool()
    yield
    await closeDbPool()
    app.state.dbPool = None


app = FastAPI(lifespan=lifespan)
app.include_router(scrapper.router)
