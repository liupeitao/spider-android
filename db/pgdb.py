# -*- coding: utf-8 -*-

# @Author   : Jingjing-Zhu
# @Time     : 2023/11/17 16:48
# @File     : pgpool.py
# @Project  : DT5
import threading
from threading import (
    BoundedSemaphore,  #: 信号量
    Lock,
)

from loguru import logger
from psycopg2 import pool
from psycopg2.extras import RealDictCursor, register_uuid

from core.config import config

register_uuid()


PG_CONF = {
    "user": config.PG_USER,
    "password": config.PG_PASSWORD,
    "host": config.PG_HOST,
    "port": config.PG_PORT,
    "database": config.PG_DB,
    "application_name": "spider",  #: 保持连接名称
    "keepalives": 1,  #: 保持连接
    "keepalives_idle": 1,  #: 空闲时，每10秒保持连接连通
    "keepalives_interval": 5,  #: 没得到回应时，等待10秒重新尝试保持连通
    "keepalives_count": 3,  #: 尝试最多5次重新保持连通
}


class PostgresPool(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with PostgresPool._instance_lock:
                if not hasattr(cls, "_instance"):
                    PostgresPool._instance = object.__new__(cls)
        return PostgresPool._instance

    def __init__(self, min_conn: int = 5, max_conn: int = 10, *args, **kwargs) -> None:
        self.min_conn = min_conn
        self.max_conn = max_conn
        self.args = args
        self.kwargs = kwargs
        if hasattr(self, "__flag"):
            return
        __lock = Lock()  #: 保证多线程只执行一次__init__
        with __lock:
            if not hasattr(self, "__flag"):
                self._semaphore = BoundedSemaphore(self.max_conn)  #: 信号量最大值
                self.POOL = pool.ThreadedConnectionPool(
                    self.min_conn, self.max_conn, *self.args, **self.kwargs
                )

            __flag: bool = True

    def _get_conn(self, key=None):
        self._semaphore.acquire()
        conn = self.POOL.getconn(key=key)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        return conn, cursor

    def _close_conn(self, conn, cursor) -> None:
        cursor.close()
        self.POOL.putconn(conn)
        try:
            self._semaphore.release()
        except ValueError as va:
            print(va, "Semaphore released too many times \n 信号量已经达到最大值！")
            self._semaphore._value = self.max_conn

    def _close_all(self):
        self.POOL.closeall()

    #: 执行增删改
    def execute(self, sql, value=None, fetch=False):
        conn, cursor = self._get_conn()
        try:
            cursor.execute(sql, value)
            conn.commit()
            if fetch:
                return cursor.fetchone()
            else:
                return []
        except Exception as e:
            print(e)
            conn.rollback()
            raise e
        finally:
            self._close_conn(conn, cursor)

    #: 查一条
    def select_one(self, sql: str, params=None):
        conn, cursor = self._get_conn()
        try:
            cursor.execute(sql, params)
            return cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            self._close_conn(conn, cursor)

    #: 查全部
    def select_all(self, sql, params=None):
        conn, cursor = self._get_conn()
        try:
            cursor.execute(sql, params)
            conn.commit()
            return cursor.fetchall()
        except Exception as e:
            conn.rollback()
            logger.error(e)
            raise e
        finally:
            self._close_conn(conn, cursor)

    #: 执行批量插入
    def executemany(self, sql, params=None, fetch=False):
        conn, cursor = self._get_conn()
        try:
            cursor.executemany(sql, params)
            conn.commit()
            if fetch:
                return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            logger.error(e)
            raise e
        finally:
            self._close_conn(conn, cursor)


pg_client = PostgresPool(**PG_CONF)
print(pg_client)
# res = pg_client.execute("select 1")
# print(res)
