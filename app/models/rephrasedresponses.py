from sqlalchemy import BigInteger, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class RephrasedResponse(Base, TimestampMixin):
    __tablename__ = 'rephrasedresponses'
    
    response_id = Column(BigInteger, primary_key = True, autoincrement = True)
    
    query_id = mapped_column(ForeignKey("userqueries.query_id"))
    response_query_name = relationship("UserQuery", back_populates="query_response", lazy="raise")

    response_text = Column(String, nullable = True)
    
    
    