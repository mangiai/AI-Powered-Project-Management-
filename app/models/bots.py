from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class Bot(Base, TimestampMixin):
    __tablename__ = 'bots'
    
    bot_id = Column(BigInteger, primary_key = True, autoincrement = True)
    bot_name = Column(String, nullable = True)
    bot_description = Column(String, nullable = True)
    
    bot_chat = relationship(
        "Chat", back_populates="chat_bot_name", lazy="raise", passive_deletes=True
    )
    