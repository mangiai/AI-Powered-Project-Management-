from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.steward import RequestSteward, ResponseSteward, ListResponseSteward
import database.steward as lc


steward_router = APIRouter(
    prefix="/steward",
)


@steward_router.get("/", response_model=ListResponseSteward)
def get_steward(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    steward = lc.get_steward(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": steward}


@steward_router.post("/", response_model=ResponseSteward, status_code=status.HTTP_201_CREATED)
def create_steward(steward: RequestSteward, db: Session = Depends(get_db)):
    lc.create_steward(db, steward)
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": steward}


@steward_router.get("/{steward_id}", response_model=ResponseSteward)
def retrieve_steward(steward_id: int = Path(...), db: Session = Depends(get_db)):
    db_steward = lc.get_steward_by_id(db, steward_id=steward_id)
    if db_steward is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="steward not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_steward}


@steward_router.put("/{steward_id}", response_model=ResponseSteward)
def update_steward(steward_id: int = Path(...), steward: RequestSteward = None, db: Session = Depends(get_db)):
    db_steward = lc.get_steward_by_id(db, steward_id=steward_id)
    if db_steward is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="steward not found")
    lc.update_steward(db, steward_id=steward_id, steward=steward)
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_steward}


@steward_router.delete("/{steward_id}", response_model=ResponseSteward)
def delete_steward(steward_id: int = Path(...), db: Session = Depends(get_db)):
    db_steward = lc.get_steward_by_id(db, steward_id=steward_id)
    if db_steward is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="steward not found")
    lc.delete_steward(db, steward_id=steward_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "steward deleted"}