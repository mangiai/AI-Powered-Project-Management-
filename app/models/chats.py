from sqlalchemy import BigInteger, Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class Chat(Base, TimestampMixin):
    __tablename__ = 'chats'
    
    chat_id = Column(BigInteger, primary_key = True, autoincrement = True)
    
    bot_id = mapped_column(ForeignKey("bots.bot_id"))
    chat_bot_name = relationship("Bot", back_populates="bot_chat", lazy="raise")

    user_id = mapped_column(ForeignKey("users.id"))
    chat_user_name = relationship("User", back_populates="user_chat", lazy="raise")

    chat_msg = relationship(
        "Msg", back_populates="msg_chat_name", lazy="raise", passive_deletes=True
    )
    