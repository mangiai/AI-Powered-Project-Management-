from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.lifecycle import RequestLifecycle, ResponseLifecycle, ListResponseLifecycle
import database.lifecycle as lc


lifecycle_router = APIRouter(
    prefix="/lifecycle",
)


@lifecycle_router.get("/", response_model=ListResponseLifecycle)
def get_lifecycle(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    lifecycle = lc.get_lifecycle(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": lifecycle}


@lifecycle_router.post("/", response_model=ResponseLifecycle, status_code=status.HTTP_201_CREATED)
def create_lifecycle(lifecycle: RequestLifecycle, db: Session = Depends(get_db)):
    lc.create_lifecycle(db, lifecycle)
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": lifecycle}


@lifecycle_router.get("/{lifecycle_id}", response_model=ResponseLifecycle)
def retrieve_lifecycle(lifecycle_id: int = Path(...), db: Session = Depends(get_db)):
    db_lifecycle = lc.get_lifecycle_by_id(db, lifecycle_id=lifecycle_id)
    if db_lifecycle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="lifecycle not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_lifecycle}


@lifecycle_router.put("/{lifecycle_id}", response_model=ResponseLifecycle)
def update_lifecycle(lifecycle_id: int = Path(...), lifecycle: RequestLifecycle = None, db: Session = Depends(get_db)):
    db_lifecycle = lc.get_lifecycle_by_id(db, lifecycle_id=lifecycle_id)
    if db_lifecycle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="lifecycle not found")
    lc.update_lifecycle(db, lifecycle_id=lifecycle_id, lifecycle=lifecycle)
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_lifecycle}


@lifecycle_router.delete("/{lifecycle_id}", response_model=ResponseLifecycle)
def delete_lifecycle(lifecycle_id: int = Path(...), db: Session = Depends(get_db)):
    db_lifecycle = lc.get_lifecycle_by_id(db, lifecycle_id=lifecycle_id)
    if db_lifecycle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="lifecycle not found")
    lc.delete_lifecycle(db, lifecycle_id=lifecycle_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "lifecycle deleted"}