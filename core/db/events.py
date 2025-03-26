'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-12-04 15:35:44
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 15:43:47
FilePath: /spider-android/core/db/events.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from config.settings import BaseConfig
from fastapi import FastAPI
from loguru import logger




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
