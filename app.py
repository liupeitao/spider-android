from contextlib import asynccontextmanager

import uvicorn
from config import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tools.helper import banner
from tools.logger import creat_customize_log_loguru

from events import create_start_app_handler, create_stop_app_handler
from routes.api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    banner("Hi QcSpider")
    creat_customize_log_loguru()
    await create_start_app_handler(app, config)
    yield
    await create_stop_app_handler(app)
    banner("Bye Closed")


def get_application(prefix) -> FastAPI:
    app = FastAPI(lifespan=lifespan, redoc_url=None)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=prefix)
    return app


app = get_application("/api/v1/Task")


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.9.31", port=7002, log_level="info")
