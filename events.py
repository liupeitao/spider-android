import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Coroutine

from config.settings import BaseConfig
from fastapi import FastAPI
from loguru import logger

from core.db.events import (
    close_mongo_connection,
    close_pg_connection,
    connect_to_mongo,
    connect_to_pg,
)


def create_start_app_handler(app: FastAPI, settings: BaseConfig) -> Coroutine:
    async def start_app() -> None:
        async with asyncio.TaskGroup() as tg:
            pg_pool = tg.create_task(connect_to_pg(settings))
            mg_pool = tg.create_task(connect_to_mongo(settings))
        app.state.pool = await pg_pool
        app.state.mongo = await mg_pool
        app.state.key_db = {}

    app.state.process_pool = ProcessPoolExecutor()
    return start_app()


def create_stop_app_handler(app: FastAPI) -> Coroutine:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        await close_pg_connection(app)
        close_mongo_connection(app)

    asyncio.to_thread
    return stop_app()
