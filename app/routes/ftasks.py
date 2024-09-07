from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import join
from schemas.ftasks import FTaskCreateSchema, FTaskReadSchema, FTaskUpdateSchema, ResponseFTaskSchema, ListResponseFTaskSchema
import database.ftasks as tc

ftask_router = APIRouter(
    prefix="/ftasks",
)


@ftask_router.get("/", response_model=ListResponseFTaskSchema, summary="Get FTasks")
def get_tasks(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, project_id: int = None, current_status: int = None):
    ftasks = tc.get_ftasks(db, skip=skip, limit=limit, project_id=project_id, current_status=current_status)
    return {"code": "success", "status": status.HTTP_200_OK, "response": ftasks}


@ftask_router.post("/", response_model=ResponseFTaskSchema, status_code=status.HTTP_201_CREATED)
def create_ftask(ftask: FTaskCreateSchema, db: Session = Depends(get_db)):
    returned_data = FTaskReadSchema.model_validate(tc.create_ftask(db, ftask))

    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@ftask_router.get("/{ftask_id}", response_model=ResponseFTaskSchema)
def retrieve_ftask(ftask_id: int = Path(...), db: Session = Depends(get_db)):
    db_ftask = tc.get_ftask_by_id(db, ftask_id=ftask_id)
    if db_ftask is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ftask not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_ftask}


@ftask_router.put("/{ftask_id}", response_model=ResponseFTaskSchema)
def update_ftask(ftask_id: int = Path(...), ftask: FTaskUpdateSchema = None, db: Session = Depends(get_db)):
    db_ftask = tc.get_ftask_by_id(db, ftask_id=ftask_id)
    if db_ftask is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ftask not found")
    returned_data = FTaskReadSchema.model_validate(tc.update_ftask(db, ftask_id=ftask_id, ftask=ftask))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@ftask_router.delete("/{ftask_id}", response_model=ResponseFTaskSchema)
def delete_ftask(ftask_id: int = Path(...), db: Session = Depends(get_db)):
    db_task = tc.get_ftask_by_id(db, ftask_id=ftask_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ftask not found")
    tc.delete_ftask(db, ftask_id=ftask_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "ftask deleted"}