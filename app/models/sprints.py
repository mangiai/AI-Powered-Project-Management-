from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Integer, Date, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class Sprint(Base, TimestampMixin):
    __tablename__ = 'sprints'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)
    retro = Column(String(1000), nullable= True)
    is_completed = Column(Boolean, default=False, nullable=True)
    StartDate = Column(Date, nullable=True)
    EndDate = Column(Date, nullable=True)
    
    sprint_lifecycle_id = mapped_column(ForeignKey("lifecycle.id"))
    lifecycle_sprint_name = relationship("Lifecycle", back_populates="lifecycle_sprint", lazy="raise") 
    
    release_id = mapped_column(ForeignKey("releases.id"))
    release_name = relationship(
        "Release", back_populates="release", lazy="raise"
    ) 
    
    sprint_story = relationship(
        "Story", back_populates="sprint_story_name", lazy="raise", passive_deletes=True
    ) 
    # proj_risks = relationship(
    #     "Risk", back_populates="risk_proj_name", lazy="raise", passive_deletes=True
    # )

    
    