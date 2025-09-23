from contextlib import asynccontextmanager
from fastapi import FastAPI
from scrapper import router as scrapper
from users import router as users
from auth import router as auth
from database import getDbPool, closeDbPool
from utils.taskSaveTasas import taskSaveTasas
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await getDbPool()
    app.state.dbPool = pool
    app
    asyncio.create_task(taskSaveTasas(36000, pool))
    yield
    await closeDbPool()
    app.state.dbPool = None


app = FastAPI(lifespan=lifespan)
app.include_router(scrapper.router)
app.include_router(users.router)
app.include_router(auth.router)
