import datetime
import json
from typing import Callable

from uuid import UUID
import requests
from loguru import logger

# success_sql = """ INSERT INTO task (taskuid ,app,state,"group",  "progress", created_at) VALUES (%s,%s,'成功',%s,%s, %s) RETURNING id;"""
# error_sql = """ INSERT INTO task (taskuid ,app,state,"group","progress", reason, created_at) VALUES (%s,%s,'失败',%s,%s, %s, %s) RETURNING id;"""
from config.settings import config
from core.db.models import (
    FUNCTION_REPRESENT,
    LogModel,
    ScrollModel,
    StateEnum,
    SwitchPageOpModel,
)
aiohttp_session = requests.session()


def cancel_all_tasks(spider):
    for t in spider.tasks:
        t.cancel()

def get_string_from_func(func: str | Callable) -> str:
    if isinstance(func, str):
        new_str = func
        if func.startswith("crawl_"):
            new_str = func.replace("crawl_", "")
        return FUNCTION_REPRESENT.get(new_str, new_str)
    else:
        new_str = func.__name__
        if func.__name__.startswith("crawl_"):
            new_str = func.__name__.replace("crawl_", "")
        return FUNCTION_REPRESENT.get(new_str, new_str)


def send_log(item: LogModel, group):
    if item.state == StateEnum.ERROR or item.msg:
        state = "失败"
    else:
        state = "成功"
    with open("log.json", "a") as f:
        f.write(
            json.dumps(
                {
                    "taskuid": str(item.app.task_uid),
                    "app": item.app.app,
                    "group": group,
                    "state": state,
                    "progress": 1,
                    "create_time": item.create_time,
                    "error": item.msg,
                },
                ensure_ascii=False,
                indent=4,
            )
        )
    aiohttp_session.post(
        config.LOGGER_URL,
        json={
            "taskuid": str(item.app.task_uid),
            "app": item.app.app,
            "group": group,
            "state": state,
            "progress": 1,
            "create_time": item.create_time,
            "error": item.msg,
        },
    )


class State:
    state = StateEnum.PENDING

    def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        func_str = get_string_from_func(item.func)
        group = f"{func_str}:{self.state.value}"
        logger.info(f"{name}|{group}|{item.create_time}|{task_uid}")
        send_log(item, group)


class PEDING_STATE(State):
    state = StateEnum.PENDING
    pass

# 任务开始执行
# class TASK_START_STATE(State):
#     state = StateEnum.TASK_START
#     async def do(self, item: LogModel, *args, **kwargs):  #
#         task_uid: UUID = item.app.task_uid
#         name = item.app.app
#         func_str = get_string_from_func(item.func)
#         group = f"{func_str}"
#         group2 = f"{func_str}:{self.state.value}"
#         logger.info(f"{name}|{group2}|{item.create_time}|{task_uid}")
#         await send_log(item, group)    

class STARTING_STATE(State):
    state = StateEnum.STARTING
    def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        func_str = get_string_from_func(item.func)
        group = f"{func_str}:{self.state.value}"
        group2 = f"{func_str}:{self.state.value}"
        logger.info(f"{name}|{group2}|{item.create_time}|{task_uid}")
        send_log(item, group)    


class RUNNING_STATE(State):
    state = StateEnum.RUNNING
    pass


class LAUNCH_BROWSER_STATE(State):
    state = StateEnum.LAUNCH_BROWSER


class CLOSING_BROWSER_STATE(State):
    state = StateEnum.CLOSING_BROWSER
    pass


class OPEN_PAGE_STATE(State):
    state = StateEnum.OPEN_PAGE
    pass


class CLOSING_PAGE_STATE(State):
    state = StateEnum.CLOSING_PAGE
    pass


class SCROLLING_STATE(State):
    state = StateEnum.SCROLLING

    def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        try:
            scroll: ScrollModel = args[2]
            if not isinstance(scroll, ScrollModel):
                # TODO super().do()
                raise Exception("scroll is not a ScrollModel instance")
        except Exception as e:
            raise e
        crawler = scroll.crawler
        crawler_str = get_string_from_func(crawler)  # 所属爬虫 字符串， 不包含crawl_
        group = f"{crawler_str}:{self.state.value}"
        logger.info(f"{name}|{group}|{item.create_time}|{task_uid}")
        send_log(item, group)


class SWITCH_PAGE_STATE(State):
    state = StateEnum.SWITCH_PAGE

    def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        try:
            switch_page = kwargs.get("switch_page_model")
            if not isinstance(switch_page, SwitchPageOpModel):
                # TODO super().do()
                raise Exception("scroll is not a ScrollModel instance")
        except Exception as e:
            raise e
        crawler_str = get_string_from_func(
            switch_page.crawler
        )  # 所属爬虫 字符串， 不包含crawl_
        index = switch_page.index
        group = f"{crawler_str}:{self.state.value}:第{index}页"
        logger.info(f"{name}|{group}|{item.create_time}|{task_uid}")
        send_log(item, group)


class FINISHED_STATE(State):
    state = StateEnum.FINISHED

    def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        future: Future = kwargs.get("future", None)
        if future is not None:
            crawler_str = get_string_from_func(future.get_name())
        else:
            crawler_str = ""
        name = item.app.app
        group = f"{crawler_str}:{self.state.value}"
        logger.info(f"{name}|{group}|{item.create_time}|{task_uid}")
        send_log(item, group)


class CLEAN_STATE(State):
    state = StateEnum.CLEAN
    pass


class ERROR_STATE(State):
    state = StateEnum.ERROR

    def __init__(self) -> None:
        super().__init__()

    def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        func_str = get_string_from_func(item.func)
        group = f"{func_str}:{self.state.value}:{item.msg}"
        group1 = f"{func_str}"
        if item.msg is None:
            item.msg = "未知错误"
        item.msg  = f"|{self.state.value}| => " + item.msg 
        # values = [task_uid, name, group, 0.0, item.msg, item.create_time]
        # pg_client.execute(error_sql, value=values)
        logger.info(f"{item.msg}{name}|{group}|{item.create_time}|{task_uid}")
        send_log(item, group1)


class ITER_INTERFACE_STATE(State):
    state = StateEnum.ITERCEPT_URL

    def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        group = f"{self.state.value}"
        logger.info(f"{name}|{group}|{item.create_time}|{task_uid}")
        # await send_log(item, group)


class StateContext:
    def __init__(self):
        self.state = PEDING_STATE()
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def set_state(self, state: StateEnum):
        if state == StateEnum.PENDING:
            self.state = PEDING_STATE()
        if state == StateEnum.STARTING:
            self.state = STARTING_STATE()
        elif state == StateEnum.RUNNING:
            self.state = RUNNING_STATE()
        elif state == StateEnum.LAUNCH_BROWSER:
            self.state = LAUNCH_BROWSER_STATE()
        elif state == StateEnum.CLOSING_BROWSER:
            self.state = CLOSING_BROWSER_STATE()
        elif state == StateEnum.OPEN_PAGE:
            self.state = OPEN_PAGE_STATE()
        elif state == StateEnum.CLOSING_PAGE:
            self.state = CLOSING_PAGE_STATE()
        elif state == StateEnum.SCROLLING:
            self.state = SCROLLING_STATE()
        elif state == StateEnum.SWITCH_PAGE:
            self.state = SWITCH_PAGE_STATE()
        elif state == StateEnum.FINISHED:
            self.state = FINISHED_STATE()
        elif state == StateEnum.CLEAN:
            self.state = CLEAN_STATE()
        elif state == StateEnum.ITERCEPT_URL:
            self.state = ITER_INTERFACE_STATE()
        else:
            self.state = ERROR_STATE()

    def get_state(self) -> State:
        return self.state

    ### THIS IS IO BOUND OPERATION
    def do(self, app: LogModel, *args, **kwargs):
        app.create_time = self.create_time
        self.state.do(app, *args, **kwargs)
