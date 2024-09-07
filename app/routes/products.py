from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.products import ProductCreateSchema, ProductReadSchema, ProductUpdateSchema, ResponseProductSchema, ListResponseProductSchema
import database.products as lc


product_router = APIRouter(
    prefix="/product",
)


@product_router.get("/", response_model=ListResponseProductSchema)
def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    products = lc.get_products(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": products}


@product_router.post("/", response_model=ResponseProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreateSchema, db: Session = Depends(get_db)):
    returned_data = ProductReadSchema.model_validate(lc.create_product(db, product))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@product_router.get("/{product_id}", response_model=ResponseProductSchema)
def retrieve_product(product_id: int = Path(...), db: Session = Depends(get_db)):
    db_product = lc.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="product not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_product}


@product_router.put("/{product_id}", response_model=ResponseProductSchema)
def update_product(product_id: int = Path(...), product: ProductUpdateSchema = None, db: Session = Depends(get_db)):
    db_product = lc.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="product not found")
    returned_data = ProductReadSchema.model_validate(lc.update_product(db, product_id=product_id, product=product))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@product_router.delete("/{product_id}", response_model=ResponseProductSchema)
def delete_product(product_id: int = Path(...), db: Session = Depends(get_db)):
    db_product = lc.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="product not found")
    lc.delete_product(db, product_id=product_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "product deleted"}