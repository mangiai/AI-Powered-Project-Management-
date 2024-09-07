from sqlalchemy import BigInteger, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, joinedload
from sqlalchemy import join
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class UserQuery(Base, TimestampMixin):
    __tablename__ = 'userqueries'
    
    query_id = Column(BigInteger, primary_key = True, autoincrement = True)
    
    user_id = mapped_column(ForeignKey("users.id"))
    query_user_name = relationship("User", back_populates="user_query", lazy="raise")

    project_id = mapped_column(ForeignKey("projects.id"))
    query_project_name = relationship("Project", back_populates="project_query", lazy="raise")

    program_id = mapped_column(ForeignKey("programs.id"))
    query_program_name = relationship("Program", back_populates="program_query", lazy="raise")

    portfolio_id = mapped_column(ForeignKey("portfolios.id"))
    query_portfolio_name = relationship("Portfolio", back_populates="portfolio_query", lazy="raise")

    query_text = Column(String, nullable = True)

    query_sql = relationship(
        "GeneratedSql", back_populates="sql_query_name", lazy="raise", passive_deletes=True
    )

    query_response = relationship(
        "RephrasedResponse", back_populates="response_query_name", lazy="raise", passive_deletes=True
    )
    
    
    