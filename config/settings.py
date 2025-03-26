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

    # # Postgresql

    MONGO_DB = "spider"
    TG_MAIL_LOGIN_SURPORT = False #是否支持邮箱的验证码登录
    TG_USER_SESSION_DIR = Path.home() / "tgsessions" # 保存tg会话的目录
    TG_VERIFICATION_CODE_URL = "http://localhost:7002/api/v1/Task/Telegram/varification" # 从tg app中解析出验证码后， 发送到这个url，以备后续使用。
    RUN_TG_URL = "http://localhost:7003/tg" #在同步后的，启动facebook爬虫是调用qctg项目的接口的。
    
 # 仅仅13349150214这个用到gmail邮箱， 获取tg登录验证码
    SPIDER_WEB_GMAIL_VERIFY_URL = "http://localhost:7001/api/v1/Task/gamil/varyfication"
    
    IMG_DIR = Path.home() / "static" # 图片存放目录
    LAMDA_HOST = "192.168.9.7" # lamda所在的机器地址(手机或者模拟器)
    DEFAULT_PROXY_HOST = "localhost" # 用户的默认代理， 
    DEFAULT_PROXY_PORT = 7890          # 用户的默认代理端口
    REDIS_VERIFICATION_URL = "redis://:@192.168.9.25:6379/13" # redis的连接地址, 可以用来获取前端输入的验证码。
    LOGGER_URL = "http://192.168.9.25:8003/api/v2/Task/execute_log"


#: 开发环境
class LocalConfig(BaseConfig):

    MONGO_DB = "spider"
    MONGO_URL = "mongodb://root:root123456@192.168.9.37:27017/admin"
    RUN_TG_URL = "http://localhost:7003/tg"  # 用于运行指定tg 用户的url

    TG_MAIL_LOGIN_SURPORT = True
    TG_USER_SESSION_DIR = Path.home() / "tgsessions"
    SPIDER_WEB_LOGIN_PAGE = "http://localhost:7001/api/v1/Task/login/page"
    TG_VERIFICATION_CODE_URL = "http://localhost:7002/api/v1/Task/Telegram/varification"
    SPIDER_WEB_GMAIL_VERIFY_URL = "http://localhost:7001/api/v1/Task/gamil/varyfication"
    LAMDA_HOST = "192.168.9.7"
    REDIS_VERIFICATION_URL = "redis://:@192.168.9.25:6379/13"
    LOGGER_URL = "http://192.168.9.25:8003/api/v2/Task/execute_log"


#: 生产环境
class RemoteConfig(BaseConfig):
    TG_USER_SESSION_DIR = Path.home() / "tgsessions"
    # # Postgresql
    RUN_TG_URL = "http://localhost:7003/tg"  # 用于运行指定tg 用户的url
    REDISDB_IP_PORTS = "192.168.9.37:6379"
    REDISDB_USER_PASS = "root123456"
    REDISDB_DB = 0  # 0-6 测试库  8-15 正式库
    REDISDB_URL = f"redis://:{REDISDB_USER_PASS}@{REDISDB_IP_PORTS}/{REDISDB_DB}"

    MONGO_DB = "spider"
    MONGO_URL = "mongodb://root:root123456@192.168.9.37:27017/admin"
    REMOTE_PROXY = "http://192.168.9.37"
    LAMDA_HOST = "192.168.9.7"
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
