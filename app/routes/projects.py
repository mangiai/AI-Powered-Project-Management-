from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.projects import ProjectCreateSchema, ProjectReadSchema, ProjectUpdateSchema,ResponseProjectSchema, ListResponseProjectSchema
import database.projects as lc


project_router = APIRouter(
    prefix="/project",
)


@project_router.get("/", response_model=ListResponseProjectSchema)
def get_projects(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, program_id: int = None):
    projects = lc.get_projects(db, skip=skip, limit=limit, program_id = program_id)
    return {"code": "success", "status": status.HTTP_200_OK, "response": projects}


@project_router.post("/", response_model=ResponseProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreateSchema, db: Session = Depends(get_db)):
    returned_data = ProjectReadSchema.model_validate(lc.create_project(db, project))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@project_router.get("/{project_id}", response_model=ResponseProjectSchema)
def retrieve_project(project_id: int = Path(...), db: Session = Depends(get_db)):
    db_project = lc.get_project_by_id(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="project not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_project}


@project_router.put("/{project_id}", response_model=ResponseProjectSchema)
def update_project(project_id: int = Path(...), project: ProjectUpdateSchema = None, db: Session = Depends(get_db)):
    db_project = lc.get_project_by_id(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="project not found")
    returned_data = ProjectReadSchema.model_validate(lc.update_project(db, project_id=project_id, project=project))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@project_router.delete("/{project_id}", response_model=ResponseProjectSchema)
def delete_project(project_id: int = Path(...), db: Session = Depends(get_db)):
    db_project = lc.get_project_by_id(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="project not found")
    lc.delete_project(db, project_id=project_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "project deleted"}