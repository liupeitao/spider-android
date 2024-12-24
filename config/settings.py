#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   config.py
@Time    :   2024/07/24 15:08:17
@Author  :   Jingjing-Zhu
@Email   :   1079677051@qq.com
"""

import os
from pathlib import Path

from loguru import logger


class BaseConfig:
    app_name: str = "qcspider"
    BROWSER_ALIVE_TIME = 60 * 120  # 登录时浏览器存活时间， 可以主动关闭
    SCREEN_SHOT = False  # 是否截图
    REMOTE_PROXY = "http://localhost"
    basic_user_dir = Path("assets/broswer_data/00000000000")
    
    broswer_data_dir = Path("assets/broswer_data")
    REMOTE_PROXY = "http://localhost"
    
    # # Postgresql
    PG_HOST = "192.168.9.37"
    PG_PORT = 5432
    PG_DB = "postgres"
    PG_USER = "admin"
    PG_PASSWORD = "root123456"
    PG_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    PG_MIN_CONNECTION_COUNT = 3
    PG_MAX_CONNECTION_COUNT = 10

    MONGO_DB = "spider"
    REMOTE_SERVER = "http://localhost" 
    TG_MAIL_LOGIN_SURPORT=True 
    TG_USER_SESSION_DIR= Path("/home/liupeitao/tgsessions")
    TG_VERIFICATION_CODE_URL="http://192.168.9.31:7002/api/v1/Task/Telegram/varification"
    LAMDA_HOST = "192.168.9.8"
    DEFAULT_PROXY_HOST = "localhost"
    DEFAULT_PROXY_PORT =7890

#: 开发环境
class DevelopmentConfig(BaseConfig):
    basic_user_dir = Path("assets/broswer_data/00000000000")
    broswer_data_dir = Path("assets/broswer_data")
    REMOTE_PROXY = "http://localhost"

    # # Postgresql
    PG_HOST = "192.168.9.37"
    PG_PORT = 5432
    PG_DB = "postgres"
    PG_USER = "admin"
    PG_PASSWORD = "root123456"
    PG_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    PG_MIN_CONNECTION_COUNT = 3
    PG_MAX_CONNECTION_COUNT = 10

    MONGO_DB = "spider"
    MONGO_URL = "mongodb://root:root123456@192.168.9.37:27017/admin"
    REMOTE_SERVER = "http://localhost"


class HomeConfig(BaseConfig):
    basic_user_dir = Path("assets/broswer_data/00000000000")
    broswer_data_dir = Path("assets/broswer_data")
    REMOTE_PROXY = "http://localhost"

    # # Postgresql
    PG_HOST = "localhost"
    PG_PORT = 5432
    PG_DB = "postgres"
    PG_USER = "admin"
    PG_PASSWORD = "root123456"
    PG_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    PG_MIN_CONNECTION_COUNT = 3
    PG_MAX_CONNECTION_COUNT = 10

    REDISDB_IP_PORTS = "localhost:6379"
    REDISDB_USER_PASS = "root123456"
    REDISDB_DB = 0  # 0-6 测试库  8-15 正式库
    REDISDB_URL = f"redis://:{REDISDB_USER_PASS}@{REDISDB_IP_PORTS}/{REDISDB_DB}"

    MONGO_DB = "spider"
    MONGO_URL = "mongodb://root:root123456@localhost:27017/admin"
    REMOTE_SERVER = "http://localhost"


#: 生产环境
class ProductionConfig(BaseConfig):
    basic_user_dir = Path("assets/broswer_data/00000000000")
    broswer_data_dir = Path("assets/broswer_data")
    REMOTE_PROXY = "http://192.168.9.22"

    # # Postgresql
    PG_HOST = "localhost"
    PG_PORT = 5432
    PG_DB = "postgres"
    PG_USER = "admin"
    PG_PASSWORD = "root123456"

    REDISDB_IP_PORTS = "192.168.9.21:6379"
    REDISDB_USER_PASS = "root123456"
    REDISDB_DB = 0  # 0-6 测试库  8-15 正式库
    REDISDB_URL = f"redis://:{REDISDB_USER_PASS}@{REDISDB_IP_PORTS}/{REDISDB_DB}"

    MONGO_DB = "spider"
    MONGO_URL = "mongodb://root:root123456@192.168.9.22:27017/admin"
    REMOTE_PROXY = "http://192.168.9.22"


def init_config(env: str = "home") -> BaseConfig:
    if env == "dev":
        logger.info("加载开发环境配置")
        return DevelopmentConfig()
    elif env == "home":
        logger.info("加载Home环境配置")
        return HomeConfig()
    else:
        logger.info("加在生产环墫配置")
        return DevelopmentConfig()


env = os.environ.get("qcapp", "dev")

config = init_config(env)