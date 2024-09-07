from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.epics import EpicCreateSchema, EpicReadSchema, EpicUpdateSchema, ResponseEpicSchema, ListResponseEpicSchema
import database.epics as lc


epic_router = APIRouter(
    prefix="/epic",
)


@epic_router.get("/", response_model=ListResponseEpicSchema)
def get_epics(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    epics = lc.get_epics(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": epics}


@epic_router.post("/", response_model=ResponseEpicSchema, status_code=status.HTTP_201_CREATED)
def create_epic(epic: EpicCreateSchema, db: Session = Depends(get_db)):
    returned_data = EpicReadSchema.model_validate(lc.create_epic(db, epic))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@epic_router.get("/{epic_id}", response_model=ResponseEpicSchema)
def retrieve_epic(epic_id: int = Path(...), db: Session = Depends(get_db)):
    db_epic = lc.get_epic_by_id(db, epic_id=epic_id)
    if db_epic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="epic not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_epic}


@epic_router.put("/{epic_id}", response_model=ResponseEpicSchema)
def update_epic(epic_id: int = Path(...), epic: EpicUpdateSchema = None, db: Session = Depends(get_db)):
    db_epic = lc.get_epic_by_id(db, epic_id=epic_id)
    if db_epic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="epic not found")
    returned_data = EpicReadSchema.model_validate(lc.update_epic(db, epic_id=epic_id, epic=epic))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@epic_router.delete("/{epic_id}", response_model=ResponseEpicSchema)
def delete_epic(epic_id: int = Path(...), db: Session = Depends(get_db)):
    db_epic = lc.get_epic_by_id(db, epic_id=epic_id)
    if db_epic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="epic not found")
    lc.delete_epic(db, epic_id=epic_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "epic deleted"}