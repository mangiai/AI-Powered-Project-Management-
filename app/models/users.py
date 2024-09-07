from sqlalchemy import BigInteger, Boolean, Column, String, Integer, Unicode
from sqlalchemy.orm import relationship
from config import Base
from database.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=True)
    password = Column(Unicode(255), nullable=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_system_admin = Column(Boolean, default=False)
    is_fte = Column(Boolean, default=False)
    is_business_steward = Column(Boolean, default=False)
    is_resource = Column(Boolean, default=False)
    is_onshore = Column(Boolean, default=False)
    access_level = Column(Integer, default = 1)
    
    ftasks = relationship(
        "FTask", back_populates="assignee", lazy="raise", passive_deletes=True
    )

    user_cost = relationship(
        "Cost", back_populates="cost_user_name", lazy="raise", passive_deletes=True
    )

    user_chat = relationship(
        "Chat", back_populates="chat_user_name", lazy="raise", passive_deletes=True
    )

    user_csv = relationship(
        "UploadedCSV", back_populates="csv_user_name", lazy="raise", passive_deletes=True
    )

    user_query = relationship(
        "UserQuery", back_populates="query_user_name", lazy="raise", passive_deletes=True
    )

   