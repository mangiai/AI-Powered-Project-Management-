from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Integer, Date, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins.baselineTimestamp import BaselineTimestampMixin

class Baseline(Base, BaselineTimestampMixin):
    __tablename__ = 'baseline'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)
    progress = Column(Float, nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
    cost = Column(Float, nullable=False)
    phase = Column(String(50), nullable=False)
