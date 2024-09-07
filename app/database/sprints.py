from sqlalchemy.orm import Session
from models.sprints import Sprint
from schemas.sprints import SprintCreateSchema, SprintUpdateSchema


def get_sprints(db: Session, skip: int = 0, limit: int = 100, release_id = None):
    query = db.query(Sprint)
    if release_id:
        query = query.filter(Sprint.release_id == release_id)
    return query.offset(skip).limit(limit).all()


def get_sprint_by_id(db: Session, sprint_id: int):
    return db.query(Sprint).filter(Sprint.id == sprint_id).first()


def create_sprint(db: Session, sprint: SprintCreateSchema):
    db_sprint = Sprint(name=sprint.name,
                   description=sprint.description, retro = sprint.retro, is_completed=sprint.completed
                   , StartDate=sprint.StartDate, EndDate=sprint.EndDate, release_id=sprint.release_id,
                   sprint_lifecycle_id=sprint.sprint_lifecycle_id)
    db.add(db_sprint)
    db.commit()
    db.refresh(db_sprint)
    return db_sprint


def delete_sprint(db: Session, sprint_id: int):
    db_sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    db.delete(db_sprint)
    db.commit()


def update_sprint(db: Session, sprint_id: int, sprint: SprintUpdateSchema):
    db_sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    db_sprint.name = sprint.name
    db_sprint.description = sprint.description
    db_sprint.retro = sprint.retro
    db_sprint.is_completed = sprint.completed
    db_sprint.StartDate = sprint.StartDate
    db_sprint.EndDate = sprint.EndDate
    db_sprint.release_id = sprint.release_id
    db_sprint.sprint_lifecycle_id = sprint.sprint_lifecycle_id
    db.commit()
    db.refresh(db_sprint)
    return db_sprint

