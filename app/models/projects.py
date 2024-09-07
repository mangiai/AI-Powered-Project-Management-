from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Integer, Date, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = 'projects'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)
    retro = Column(String(1000), nullable= True)
    is_completed = Column(Boolean, default=False, nullable=True)
    StartDate = Column(Date, nullable=True)
    EndDate = Column(Date, nullable=True)
    
    program_id = mapped_column(ForeignKey("programs.id"))
    prog_name = relationship(
        "Program", back_populates="prog", lazy="raise"
    ) 
    
    project_lifecycle_id = mapped_column(ForeignKey("lifecycle.id"))
    lifecycle_proj_name = relationship("Lifecycle", back_populates="lifecycle_proj", lazy="raise") 
    
    proj_ftask = relationship(
        "FTask", back_populates="ftask_proj_name", lazy = "raise", passive_deletes=True
    )
    
    proj_risks = relationship(
        "Risk", back_populates="risk_proj_name", lazy="raise", passive_deletes=True
    )

    projname = relationship(
        "Steward", back_populates="asset_domain_proj", lazy="raise", passive_deletes=True
    )

    proj_roadmap = relationship(
        "Roadmap", back_populates="proj_roadmap_name", lazy="raise", passive_deletes=True
    )

    project_csv = relationship(
        "UploadedCSV", back_populates="csv_project_name", lazy="raise", passive_deletes=True
    )

    project_query = relationship(
        "UserQuery", back_populates="query_project_name", lazy="raise", passive_deletes=True
    )

    project_kpi = relationship(
        "KPIResult", back_populates="kpi_project_name", lazy="raise", passive_deletes=True
    )