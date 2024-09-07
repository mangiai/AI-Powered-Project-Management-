from sqlalchemy import BigInteger, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class UploadedCSV(Base, TimestampMixin):
    __tablename__ = 'uploadedcsvs'
    
    csv_id = Column(BigInteger, primary_key = True, autoincrement = True)
    
    user_id = mapped_column(ForeignKey("users.id"))
    csv_user_name = relationship("User", back_populates="user_csv", lazy="raise")

    project_id = mapped_column(ForeignKey("projects.id"))
    csv_project_name = relationship("Project", back_populates="project_csv", lazy="raise")

    program_id = mapped_column(ForeignKey("programs.id"))
    csv_program_name = relationship("Program", back_populates="program_csv", lazy="raise")

    portfolio_id = mapped_column(ForeignKey("portfolios.id"))
    csv_portfolio_name = relationship("Portfolio", back_populates="portfolio_csv", lazy="raise")

    file_path = Column(String, nullable = False)
    
    
    