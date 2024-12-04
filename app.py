'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-26 17:43:56
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 15:47:35
FilePath: /spider-android/app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from contextlib import asynccontextmanager

import uvicorn
from config import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.tools.helper import banner
from core.tools.logger import creat_customize_log_loguru

from events import create_start_app_handler, create_stop_app_handler
from core.routes.api import router as api_router


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
