from sqlalchemy.orm import Session
from models.products import Product
from schemas.products import ProductCreateSchema, ProductUpdateSchema


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreateSchema):
    db_product = Product(name=product.name,
                   description=product.description
                   , StartDate=product.StartDate, EndDate=product.EndDate,
                   product_lifecycle_id = product.product_lifecycle_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()


def update_product(db: Session, product_id: int, product: ProductUpdateSchema):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db_product.name = product.name
    db_product.description = product.description
    db_product.StartDate = product.StartDate
    db_product.EndDate = product.EndDate
    db_product.product_lifecycle_id = product.product_lifecycle_id
    db.commit()
    db.refresh(db_product)
    return db_product

