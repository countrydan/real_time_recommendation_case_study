from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from src.model import DataIn
from src.background_processes import BackGroundProcess

background_process = BackGroundProcess()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(background_process.process_queue_in())
    asyncio.create_task(background_process.send_from_queue_out())
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/receive', status_code=201)
async def receive_json(data: DataIn):
    await background_process.queue_in.put(data)
    return {'msg': 'received'}
