from sqlalchemy import BigInteger, Column, ForeignKey, String, Date
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from config import Base
from database.mixins import TimestampMixin


class Release(Base, TimestampMixin):
    __tablename__ = 'releases'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)

    release_lifecycle_id = mapped_column(ForeignKey("lifecycle.id"))
    lifecycle_release_name = relationship("Lifecycle", back_populates="lifecycle_release", lazy="raise") 
    
    
    product_id = mapped_column(ForeignKey("products.id"))
    product_name = relationship(
        "Product", back_populates="product", lazy="raise"
    )

    release = relationship(
        "Sprint", back_populates="release_name", lazy="raise", passive_deletes=True
    )
