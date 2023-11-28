import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from models.enums import enum_definitions

async def init():
    # Load enums
    await enum_definitions.load_definitions(global_import=True)


if asyncio.get_event_loop().is_running():
    asyncio.create_task(init())
else:
    asyncio.run(init())

from routers import test

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()

    yield


app = FastAPI(lifespan=lifespan)

v1 = FastAPI(lifespan=lifespan)

# Register routers
v1.include_router(test.router, prefix="/test")

app.mount("/api/v1", v1)


# Debugging only

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
