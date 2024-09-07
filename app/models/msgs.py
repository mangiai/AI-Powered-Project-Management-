from sqlalchemy import BigInteger, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class Msg(Base, TimestampMixin):
    __tablename__ = 'msgs'
    
    msg_id = Column(BigInteger, primary_key = True, autoincrement = True)
    
    chat_id = mapped_column(ForeignKey("chats.chat_id"))
    msg_chat_name = relationship("Chat", back_populates="chat_msg", lazy="raise")

    content = Column(String, nullable = True)
    msg_type = Column(Integer, nullable = True)

    
    