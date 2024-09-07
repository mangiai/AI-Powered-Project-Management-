from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Integer, Date, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin

class Steward(Base, TimestampMixin):
    __tablename__ = 'stewardship'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    asset_name = Column(String(255), nullable=False)
    asset_type = Column(String(255), nullable=False)
    asset_stage = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    calculation_method = Column(String(50), nullable=True)
    calculation_value = Column(Float, nullable=True)
    sor = Column(Boolean, default=False, nullable=False)
    dashboard_name = Column(String(255), nullable=False)
    business_steward_name = Column(String(100), nullable=False)
    it_custodian_name = Column(String(100), nullable=False)
    value_statement = Column(String(500), nullable=False)
    reason_code_statement = Column(String(500), nullable=False)
    project_rank = Column(Integer,nullable=False)


    portfolio_id = mapped_column(ForeignKey("portfolios.id"))
    asset_domain = relationship("Portfolio", back_populates="portname", lazy="raise") 

    program_id = mapped_column(ForeignKey("programs.id"))
    asset_domain_prog = relationship("Program", back_populates="progname", lazy="raise") 

    project_id = mapped_column(ForeignKey("projects.id"))
    asset_domain_proj = relationship("Project", back_populates="projname", lazy="raise") 

    ftask_id = mapped_column(ForeignKey("ftasks.id"))
    asset_domain_ftask = relationship("FTask", back_populates="ftaskname", lazy="raise") 
