import asyncio
import functools

from core.db.models import LogModel, StateEnum
from core.db.spiderstate import StateContext
from core.spiders.spider import Spider


def deco_log_state(state: StateEnum):
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not isinstance(args[0], Spider):
                raise Exception("args[0] is not a Spider instance")

            spider: Spider = args[0]
            log_item = LogModel(app=spider.app, func=func, state=state, spider=spider)
            context = StateContext()

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                log_item.exception = e
                log_item.msg = str(e)
                context.set_state(StateEnum.ERROR)
                asyncio.create_task(log_state(context, log_item, *args, **kwargs))
                raise e
            else:
                context.set_state(state)
                asyncio.create_task(log_state(context, log_item, *args, **kwargs))
                return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not isinstance(args[0], Spider):
                raise Exception("args[0] is not a Spider instance")

            spider: Spider = args[0]
            log_item = LogModel(app=spider.app, func=func, state=state, spider=spider)
            context = StateContext()

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                log_item.exception = e
                log_item.msg = str(e)
                context.set_state(StateEnum.ERROR)
                asyncio.create_task(log_state(context, log_item, *args, **kwargs))
                raise e
            else:
                context.set_state(state)
                asyncio.create_task(log_state(context, log_item, *args, **kwargs))
                return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


async def log_state(context: StateContext, log_item: LogModel, *args, **kwargs):
    # await context.do(log_item, *args, **kwargs)
    print(f"Log state: {log_item.state.value}")
