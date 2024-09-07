from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Integer, Date, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin

class Risk(Base, TimestampMixin):
    __tablename__ = 'risks'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=True)
    name = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    mitigation = Column(String(500), nullable=True)
    assigned_to = Column(Integer, nullable=True)
    is_completed = Column(Integer, default=1, nullable=False)
    risk_impact = Column(Integer, default = 1, nullable = True)
    risk_probablitly = Column(Integer, default = 1, nullable = True)
    DueDate = Column(Date, nullable=False)

    risk_proj_id = mapped_column(ForeignKey("projects.id"))
    risk_proj_name = relationship("Project", back_populates="proj_risks", lazy="raise") 

    risk_prog_id = mapped_column(ForeignKey("programs.id"))
    risk_prog_name = relationship("Program", back_populates="prog_risks", lazy="raise")

    risk_port_id = mapped_column(ForeignKey("portfolios.id"))
    risk_port_name = relationship("Portfolio", back_populates="port_risks", lazy="raise")

    is_active = Column(Boolean, default=True)


