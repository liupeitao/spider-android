# from datetime import datetime
# from typing import Optional

# from pypika import Parameter as CommonParameter
# from pypika import Query, Table
# from sqlalchemy import Uuid


# class Parameter(CommonParameter):
#     def __init__(self, count: int) -> None:
#         super().__init__("${0}".format(count))


# class TypedTable(Table):
#     __table__ = ""

#     def __init__(
#         self,
#         name: Optional[str] = None,
#         schema: Optional[str] = None,
#         alias: Optional[str] = None,
#         query_cls: Optional[Query] = None,
#     ) -> None:
#         if name is None:
#             if self.__table__:
#                 name = self.__table__
#             else:
#                 name = self.__class__.__name__

#         super().__init__(name, schema, alias, query_cls)


# CREATE TABLE mq.mq_task_job(
#     id SERIAL NOT NULL,
#     uid uuid NOT NULL DEFAULT gen_random_uuid(),
#     taskuid uuid NOT NULL,
#     "group" varchar(255),
#     app varchar(255) NOT NULL,
#     state varchar(255) NOT NULL,
#     error text,
#     createtime timestamp without time zone NOT NULL DEFAULT public.f_now(),
#     updatetime timestamp without time zone,
#     otherinfo jsonb,
#     tag json,
#     progress double precision DEFAULT 0
# );


# class Tasks(TypedTable):
#     __table__ = "tasks"

#     id: int
#     uuid: Uuid
#     taskuid: Uuid
#     group: str
#     app: str
#     state = str
#     error: str
#     createtime: datetime
#     updatetime: datetime
#     otherinfo: bytearray
#     tag: str
#     progress: float


# tasks = Tasks()
