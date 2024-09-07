from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.sprints import SprintCreateSchema, SprintReadSchema, SprintUpdateSchema,ResponseSprintSchema, ListResponseSprintSchema
import database.sprints as lc


sprint_router = APIRouter(
    prefix="/sprint",
)


@sprint_router.get("/", response_model=ListResponseSprintSchema)
def get_sprints(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, release_id: int = None):
    sprints = lc.get_sprints(db, skip=skip, limit=limit, release_id = release_id)
    return {"code": "success", "status": status.HTTP_200_OK, "response": sprints}


@sprint_router.post("/", response_model=ResponseSprintSchema, status_code=status.HTTP_201_CREATED)
def create_sprint(sprint: SprintCreateSchema, db: Session = Depends(get_db)):
    returned_data = SprintReadSchema.model_validate(lc.create_sprint(db, sprint))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@sprint_router.get("/{sprint_id}", response_model=ResponseSprintSchema)
def retrieve_sprint(sprint_id: int = Path(...), db: Session = Depends(get_db)):
    db_sprint = lc.get_sprint_by_id(db, sprint_id=sprint_id)
    if db_sprint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="sprint not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_sprint}


@sprint_router.put("/{sprint_id}", response_model=ResponseSprintSchema)
def update_sprint(sprint_id: int = Path(...), sprint: SprintUpdateSchema = None, db: Session = Depends(get_db)):
    db_sprint = lc.get_sprint_by_id(db, sprint_id=sprint_id)
    if db_sprint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="sprint not found")
    returned_data = SprintReadSchema.model_validate(lc.update_sprint(db, sprint_id=sprint_id, sprint=sprint))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@sprint_router.delete("/{sprint_id}", response_model=ResponseSprintSchema)
def delete_sprint(sprint_id: int = Path(...), db: Session = Depends(get_db)):
    db_sprint = lc.get_sprint_by_id(db, sprint_id=sprint_id)
    if db_sprint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="sprint not found")
    lc.delete_sprint(db, sprint_id=sprint_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "sprint deleted"}