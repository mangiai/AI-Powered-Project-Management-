from sqlalchemy import BigInteger, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class FTask(Base, TimestampMixin):
    __tablename__ = 'ftasks'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    wbs = Column(String(255), nullable=True)
    current_status = Column(Integer, nullable=True)
    Resource = Column(String, nullable=True)
    ActualResource = Column(String, nullable=True)
    
    PlannedStartDate = Column(DateTime, nullable=True)
    PlannedEndDate = Column(DateTime, nullable=True)
    ActualStartDate = Column(DateTime, nullable=True)
    ActualEndDate = Column(DateTime, nullable=True)
    action = Column(String(255), nullable=True)
    predecessor_successor = Column(String(255), nullable=True)
    progress = Column(Integer, nullable=True)

    assigned_to = mapped_column(ForeignKey("users.id"))
    assignee = relationship("User", back_populates="ftasks", lazy="raise")
    
    proj_id = mapped_column(ForeignKey("projects.id"))
    ftask_proj_name = relationship("Project", back_populates="proj_ftask", lazy="raise")
    
    ftask_cost = relationship(
        "Cost", back_populates="cost_ftask_name", lazy="raise", passive_deletes=True
    )

    ftaskname = relationship(
        "Steward", back_populates="asset_domain_ftask", lazy="raise", passive_deletes=True
    )