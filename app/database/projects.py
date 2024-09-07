from sqlalchemy.orm import Session
from models.projects import Project
from schemas.projects import ProjectCreateSchema, ProjectUpdateSchema


def get_projects(db: Session, skip: int = 0, limit: int = 100, program_id: int = None):
    query = db.query(Project)
    if program_id:
        query = query.filter(Project.program_id == program_id)
    return query.offset(skip).limit(limit).all()
    

def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, project: ProjectCreateSchema):
    db_project = Project(name=project.name,
                   description=project.description, retro = project.retro, is_completed=project.completed
                   , StartDate=project.StartDate, EndDate=project.EndDate, program_id=project.program_id,
                   project_lifecycle_id=project.project_lifecycle_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    db.delete(db_project)
    db.commit()


def update_project(db: Session, project_id: int, project: ProjectUpdateSchema):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    db_project.name = project.name
    db_project.description = project.description
    db_project.retro = project.retro
    db_project.is_completed = project.completed
    db_project.StartDate = project.StartDate
    db_project.EndDate = project.EndDate
    db_project.program_id = project.program_id
    db_project.project_lifecycle_id = project.project_lifecycle_id
    db.commit()
    db.refresh(db_project)
    return db_project

