from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class BaselineTimestampMixin:
    @declared_attr
    def baseline(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    