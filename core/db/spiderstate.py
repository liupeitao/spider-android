import datetime
from uuid import UUID

from core.db.models import LogModel, ScrollModel, StateEnum, SwitchPageOpModel
from core.db.pgdb import pg_client

success_sql = """ INSERT INTO task (taskuid ,app,state,"group",  "progress", created_at) VALUES (%s,%s,'成功',%s,%s, %s) RETURNING id;"""
error_sql = """ INSERT INTO task (taskuid ,app,state,"group","progress", reason, created_at) VALUES (%s,%s,'失败',%s,%s, %s, %s) RETURNING id;"""


class State:
    state = StateEnum.PENDING

    async def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        group = f"{item.func.__name__}:{self.state.value}"
        values = [task_uid, name, group, 0.0, item.create_time]
        pg_client.execute(success_sql, value=values)


class PEDING_STATE(State):
    state = StateEnum.PENDING
    pass


class STARTING_STATE(State):
    state = StateEnum.STARTING
    pass


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

    async def do(self, item: LogModel, *args, **kwargs):  #
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

        group = f"{crawler}:{item.func.__name__}:{self.state.value}"
        values = [task_uid, name, group, 0.0, item.create_time]
        pg_client.execute(success_sql, value=values)


class SWITCH_PAGE_STATE(State):
    state = StateEnum.SWITCH_PAGE

    async def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        try:
            switch_page = kwargs.get("switch_page_model")
            if not isinstance(switch_page, SwitchPageOpModel):
                # TODO super().do()
                raise Exception("scroll is not a ScrollModel instance")
        except Exception as e:
            raise e
        crawler = switch_page.crawler
        index = switch_page.index
        group = f"{crawler}:{item.func.__name__}:{self.state.value}:第{index}页"
        values = [task_uid, name, group, 0.0, item.create_time]
        pg_client.execute(success_sql, value=values)


class FINISHED_STATE(State):
    state = StateEnum.FINISHED
    pass


class CLEAN_STATE(State):
    state = StateEnum.CLEAN
    pass


class ERROR_STATE(State):
    state = StateEnum.ERROR

    def __init__(self) -> None:
        super().__init__()

    async def do(self, item: LogModel, *args, **kwargs):  #
        task_uid: UUID = item.app.task_uid
        name = item.app.app
        group = f"{item.func.__name__}:{self.state.value}"
        if item.msg is None:
            item.msg = "未知错误"
        values = [task_uid, name, group, 0.0, item.msg, item.create_time]
        pg_client.execute(error_sql, value=values)


class ITER_INTERFACE_STATE(State):
    state = StateEnum.ITERCEPT_URL


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
    async def do(self, app: LogModel, *args, **kwargs):
        app.create_time = self.create_time
        await self.state.do(app, *args, **kwargs)
