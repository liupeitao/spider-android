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
    TG_USER_SESSION_DIR= Path.home()/"tgsessions"
    TG_VERIFICATION_CODE_URL="http://localhost:7002/api/v1/Task/Telegram/varification"
    RUN_TG_URL= "http://localhost:7003/tg"

    SPIDER_LOGIN_PAGE = "http://localhost:7001/api/v1/Task/login/page"
    SPIDER_WEB_GMAIL_VERIFY_URL = "http://localhost:7001/api/v1/Task/gamil/varyfication"
    LAMDA_HOST = "192.168.9.3"
    DEFAULT_PROXY_HOST = "localhost"
    DEFAULT_PROXY_PORT =7890
    REDIS_VERIFICATION_URL = "redis://:@192.168.9.25:6379/13"
    LOGGER_URL = "http://192.168.9.25:8003/api/v2/Task/execute_log" 

#: 开发环境
class LocalConfig(BaseConfig):
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
    RUN_TG_URL= "http://localhost:7003/tg" # 用于运行指定tg 用户的url
    
    TG_MAIL_LOGIN_SURPORT=True 
    TG_USER_SESSION_DIR= Path.home()/"tgsessions"
    SPIDER_WEB_LOGIN_PAGE = "http://localhost:7001/api/v1/Task/login/page"
    TG_VERIFICATION_CODE_URL="http://localhost:7002/api/v1/Task/Telegram/varification"
    IMG_DIR = Path.home()/"static"
    SPIDER_WEB_GMAIL_VERIFY_URL = "http://localhost:7001/api/v1/Task/gamil/varyfication"
    LAMDA_HOST = "192.168.9.3"
    REDIS_VERIFICATION_URL = "redis://:@192.168.9.25:6379/13"
    LOGGER_URL = "http://192.168.9.25:8003/api/v2/Task/execute_log" 

#: 生产环境
class RemoteConfig(BaseConfig):
    basic_user_dir = Path("assets/broswer_data/00000000000")
    broswer_data_dir = Path("assets/broswer_data")
    REMOTE_PROXY = "http://192.168.9.37"
    IMG_DIR = Path.home()/"static"

    TG_USER_SESSION_DIR= Path.home()/"tgsessions"
    # # Postgresql
    PG_HOST = "localhost"
    PG_PORT = 5432
    PG_DB = "postgres"
    PG_USER = "admin"
    PG_PASSWORD = "root123456"
    RUN_TG_URL= "http://localhost:7003/tg" # 用于运行指定tg 用户的url
    REDISDB_IP_PORTS = "192.168.9.37:6379"
    REDISDB_USER_PASS = "root123456"
    REDISDB_DB = 0  # 0-6 测试库  8-15 正式库
    REDISDB_URL = f"redis://:{REDISDB_USER_PASS}@{REDISDB_IP_PORTS}/{REDISDB_DB}"

    MONGO_DB = "spider"
    MONGO_URL = "mongodb://root:root123456@192.168.9.37:27017/admin"
    REMOTE_PROXY = "http://192.168.9.37"
    LAMDA_HOST = "192.168.9.3"
    REDIS_VERIFICATION_URL = "redis://:@192.168.9.25:6379/13"
    LOGGER_URL = "http://192.168.9.25:8003/api/v2/Task/execute_log" 

def init_config(env: str = "home") -> BaseConfig:
    if env == "dev":
        logger.info("加载开发环境配置")
        return LocalConfig()
    else:
        logger.info("加在生产环墫配置")
        return LocalConfig()


env = os.environ.get("qcapp", "dev")

config = init_config(env)
if not config.IMG_DIR.exists():
    config.IMG_DIR.mkdir(exist_ok=True)
