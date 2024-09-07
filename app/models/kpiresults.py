from sqlalchemy import BigInteger, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class KPIResult(Base, TimestampMixin):
    __tablename__ = 'kpiresults'
    
    kpi_id = Column(BigInteger, primary_key = True, autoincrement = True)
    
    project_id = mapped_column(ForeignKey("projects.id"))
    kpi_project_name = relationship("Project", back_populates="project_kpi", lazy="raise")

    program_id = mapped_column(ForeignKey("programs.id"))
    kpi_program_name = relationship("Program", back_populates="program_kpi", lazy="raise")

    portfolio_id = mapped_column(ForeignKey("portfolios.id"))
    kpi_portfolio_name = relationship("Portfolio", back_populates="portfolio_kpi", lazy="raise")

    cost_kpi = Column(String, nullable = True)
    project_kpi = Column(String, nullable = True)
    risk_kpi = Column(String, nullable = True)


    
    
    