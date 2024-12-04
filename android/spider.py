'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-12-04 09:38:12
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 10:01:46
FilePath: /spider-android/android/spider.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import asyncio
import datetime
import os
from abc import abstractmethod
from asyncio import Task
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional, Self

from const import CRAWLER_DEFINE
from db.models import App, BaseInfoModel, CrawlerInfoModel
from deps.ref import object_ref
def transform_phone_to_port(phone):
    return phone

class Spider(object_ref):
    def __init__(
        self,
        app: App = App(),
    ):
        super().__init__()
        self.app: App = app
        self.name: str = app.app
        self.screen_name = CRAWLER_DEFINE.get(self.name, self.name)
        self.login_url: str = app.login_url
        self.phone: str = app.phone
        self.port = app.port
        self.task_uid = app.task_uid
        self.countrycode = app.countrycode
        self.lock = asyncio.Lock()
        self.pid: int = os.getpid()
        self.tasks: list[asyncio.Task] = []
        if self.port is None:
            self.port = transform_phone_to_port(phone=self.phone)
        self.save_dir: Path = Path.home() / "smbshare"
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True, exist_ok=True)

    def get_save_path(self, crawl: str, suffix="json") -> Path:
        self.save_path_format = "{countrycode}{phone}_{name}_{time}_{crawl}.{suffix}"
        return self.save_dir / self.save_path_format.format(
            countrycode=self.countrycode,
            phone=self.phone,
            name=self.name,
            time=int(datetime.datetime.now().timestamp()),
            crawl=crawl,
            suffix=suffix,
        )

    @abstractmethod
    async def start(self, tasks: Optional[list[str]] = None):
        pass

    @abstractmethod
    def pipline(self, future: Task) -> None:
        pass

    @abstractmethod
    async def close(self):
        pass

    @lru_cache
    def get_crawl_functions(self) -> list[str]:
        return [func for func in self.get_all_functions() if func.startswith("crawl")]

    @lru_cache
    def get_all_functions(self) -> list[str]:
        return [
            func
            for func in dir(self)
            if callable(getattr(self, func))
            and func.startswith("crawl")
            and not func.startswith("_")
        ]

    def start_requests(self) -> list[str]:
        return self.get_crawl_functions()

    def _set_crawler(self, crawler) -> None:
        self.crawler = crawler
        self.settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler, *args: Any, **kwargs: Any) -> Self:
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def get_extra(self) -> CrawlerInfoModel:
        extra = BaseInfoModel(
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sid=os.uname().sysname,
            source=self.screen_name,
            user_phone_number=self.countrycode + self.phone,
            phone_number=self.phone,
        )
        extra = CrawlerInfoModel(crawlerinfo=extra)
        return extra
