from sqlalchemy import BigInteger, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class Cost(Base, TimestampMixin):
    __tablename__ = 'costs'
    
    id = Column(BigInteger, primary_key = True, autoincrement = True)
    cost_per_hour = Column(Integer, nullable = True)
    total_hours = Column(Integer, nullable = True)
    fixed_cost = Column(Integer, nullable = True)
    actual_hours = Column(Integer, nullable = True)
    actual_fixed_cost = Column(Integer, nullable = True)
    
    cost_ftask_id = mapped_column(ForeignKey("ftasks.id"))
    cost_ftask_name = relationship("FTask", back_populates="ftask_cost", lazy="raise") 
  
    cost_user_id = mapped_column(ForeignKey("users.id"))
    cost_user_name = relationship("User", back_populates="user_cost", lazy="raise") 

    cost_story_id = mapped_column(ForeignKey("stories.id"))
    cost_story_name = relationship("Story", back_populates="story_cost", lazy="raise") 

    location = Column(Integer, nullable=True)
