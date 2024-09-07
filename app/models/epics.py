from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr
from config import Base


class Epic(Base):
    __tablename__ = 'epics'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    themename = Column(String(255), nullable=True)
    
    epic_story = relationship(
        "Story", back_populates="epic_story_name", lazy="raise", passive_deletes=True
    )
