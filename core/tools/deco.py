import asyncio
import functools

from core.db.models import LogModel, StateEnum
from core.db.spiderstate import StateContext
from core.spider import Spider


def deco_log_state(state: StateEnum):
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not isinstance(args[0], Spider):
                raise Exception("args[0] is not a Spider instance")

            spider: Spider = args[0]
            log_item = LogModel(app=spider.app, func=func, state=state, spider=spider)
            context = StateContext()
            
            context.set_state(state)
            log_state(context, log_item, *args, **kwargs)
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                log_item.exception = e
                log_item.msg = str(e)
                context.set_state(StateEnum.ERROR)
                log_state(context, log_item, *args, **kwargs)
                raise e
            else:
                return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not isinstance(args[0], Spider):
                raise Exception("args[0] is not a Spider instance")

            spider: Spider = args[0]
            log_item = LogModel(app=spider.app, func=func, state=state, spider=spider)
            context = StateContext()
            context.set_state(state)
            log_state(context, log_item, *args, **kwargs)
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                log_item.exception = e
                log_item.msg = str(e)
                context.set_state(StateEnum.ERROR)
                log_state(context, log_item, *args, **kwargs)
                raise e
            else:
                context.set_state(state)
                log_state(context, log_item, *args, **kwargs)
                return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def log_state(context: StateContext, log_item: LogModel, *args, **kwargs):
    context.do(log_item, *args, **kwargs)
