from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Date, Integer, Float
from sqlalchemy.orm import relationship, mapped_column
from config import Base
from database.mixins import TimestampMixin

class Story(Base, TimestampMixin):
    __tablename__ = 'stories'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=False)
    typeofstory = Column(Integer, nullable = True)

    name = Column(String(100), nullable=False)
    iwantto = Column(String(500), nullable=True)
    solcan = Column(String(500), nullable=True)
    acceptancecriteria = Column(String(500), nullable=True)
    priority = Column(Integer, nullable = True)

    assigned_to = Column(BigInteger, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=True)
    current_status = Column(Integer, default = 1, nullable = True)
    velocityPoints = Column(Integer, nullable=True)
    sprint = Column(Float, nullable=True)
    taskDuration=Column(Integer, nullable=True)
    
    resource = Column(String, nullable=True)
    actualResource = Column(String, nullable=True)

    actualStartDate = Column(Date, nullable=True)
    actualEndDate=Column(Date, nullable=True)

    plannedStartDate = Column(Date, nullable=True)
    plannedEndDate = Column(Date, nullable=True)
    
    sprint_id = mapped_column(ForeignKey("sprints.id"))
    sprint_story_name = relationship("Sprint", back_populates="sprint_story", lazy="raise") 

    epic_id = mapped_column(ForeignKey("epics.id"))
    epic_story_name = relationship("Epic", back_populates="epic_story", lazy="raise") 

    story_cost = relationship(
        "Cost", back_populates="cost_story_name", lazy="raise", passive_deletes=True
    )