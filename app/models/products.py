from sqlalchemy import BigInteger, Column, ForeignKey, String, Date
from sqlalchemy.orm import relationship, mapped_column
from config import Base
from database.mixins import TimestampMixin

class Product(Base, TimestampMixin):
    __tablename__ = 'products'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)

    product_lifecycle_id = mapped_column(ForeignKey("lifecycle.id"))
    lifecycle_product_name = relationship(
        "Lifecycle", back_populates="lifecycle_product", lazy="raise"
    )

    product = relationship(
        "Release", back_populates="product_name", lazy="raise", passive_deletes=True
    )

    
