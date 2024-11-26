from typing import Optional

import asyncpg
from asyncpg import Pool
from config.settings import BaseConfig
from fastapi import FastAPI
from loguru import logger


async def connect_to_pg(settings: Optional[BaseConfig] = None) -> Pool:
    pool = None

    async def get_pool(existing_pool) -> Pool:
        if existing_pool is not None:
            return existing_pool
        logger.info("Connecting to PostgreSQL")
        if settings is None:
            raise ValueError("Settings is required")
        pool = await asyncpg.create_pool(
            str(settings.PG_URL),
            min_size=settings.PG_MIN_CONNECTION_COUNT,
            max_size=settings.PG_MAX_CONNECTION_COUNT,
        )
        if pool is None:
            raise ConnectionError("Could not connect to PostgreSQL")
        logger.info("Postgresql Connection established")
        return pool

    return await get_pool(pool)


async def close_pg_connection(app: FastAPI) -> None:
    logger.info(" Closing Postgresql connection to database")

    await app.state.pool.close()

    logger.info("Postgresql Connection closed")


async def connect_to_mongo(settings: BaseConfig):
    from motor.motor_asyncio import AsyncIOMotorClient

    MONGO_URL = settings.MONGO_URL
    client = AsyncIOMotorClient(MONGO_URL)
    logger.info("MongoDB Connection established")
    return client


def close_mongo_connection(app: FastAPI) -> None:
    logger.info("Closing connection to MongoDB")
    print(app.state.mongo)
    print("-==================================")
    app.state.mongo.close()
    logger.info("MongoDB Connection closed")
