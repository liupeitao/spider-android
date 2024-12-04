# from sqlmodel import UUID, DateTime, Field, SQLModel
import uuid
from datetime import datetime

from pydantic import BaseModel


class LogModel(BaseModel):
    taskuid: uuid.UUID = uuid.uuid4()
    status: str = ""
    app: str = ""
    stage: str = ""
    detail: str = ""
    created_at: datetime = datetime.now()
