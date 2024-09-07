from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from config import Base  # Ensure this matches your actual Base import
from database.mixins import TimestampMixin

class Roadmap(Base, TimestampMixin):
    __tablename__ = 'roadmaps'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    project_id = mapped_column(ForeignKey("projects.id"))
    proj_roadmap_name = relationship("Project", back_populates="proj_roadmap", lazy="raise") 
    
    program_id = mapped_column(ForeignKey("programs.id"))
    prog_roadmap_name = relationship("Program", back_populates="prog_roadmap", lazy="raise") 

    portfolio_id = mapped_column(ForeignKey("portfolios.id"))
    port_roadmap_name = relationship("Portfolio", back_populates="port_roadmap", lazy="raise")

    is_active = Column(Boolean, default=True)

