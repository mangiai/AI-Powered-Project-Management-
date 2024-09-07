from sqlalchemy.orm import Session
from models.ftasks import FTask
from schemas.ftasks import FTaskCreateSchema, FTaskUpdateSchema




def get_ftasks(db: Session, skip: int = 0, limit: int = 100, project_id: int = None, current_status: int = None):
  query = db.query(FTask)
  if project_id:
    query = query.filter(FTask.proj_id == project_id)
  if current_status:
    query = query.filter(FTask.current_status == current_status)
  return query.offset(skip).limit(limit).all()


def get_ftask_by_id(db: Session, ftask_id: int):
    return db.query(FTask).filter(FTask.id == ftask_id).first()


def create_ftask(db: Session, ftask: FTaskCreateSchema):
    db_FTask = FTask(name=ftask.name,
                   description=ftask.description, wbs = ftask.wbs, current_status = ftask.current_status, Resource = ftask.Resource,
                   ActualResource=ftask.ActualResource, PlannedStartDate = ftask.PlannedStartDate, PlannedEndDate = ftask.PlannedEndDate,
                   ActualStartDate = ftask.ActualStartDate, ActualEndDate = ftask.ActualEndDate,
                   action = ftask.action,
                   predecessor_successor = ftask.predecessor_successor,
                   progress = ftask.progress, assigned_to = ftask.assigned_to, proj_id = ftask.proj_id)
    db.add(db_FTask)
    db.commit()
    db.refresh(db_FTask)
    return db_FTask


def delete_ftask(db: Session, ftask_id: int):
    db_FTask = db.query(FTask).filter(FTask.id == ftask_id).first()
    db.delete(db_FTask)
    db.commit()


def update_ftask(db: Session, ftask_id: int, ftask: FTaskUpdateSchema):
    db_FTask = db.query(FTask).filter(FTask.id == ftask_id).first()
    db_FTask.name = ftask.name
    db_FTask.description = ftask.description
    db_FTask.wbs = ftask.wbs
    db_FTask.current_status = ftask.current_status
    db_FTask.Resource = ftask.Resource
    db_FTask.ActualResource = ftask.ActualResource
    db_FTask.PlannedStartDate = ftask.PlannedStartDate
    db_FTask.PlannedEndDate = ftask.PlannedEndDate
    db_FTask.ActualStartDate = ftask.ActualStartDate
    db_FTask.ActualEndDate = ftask.ActualEndDate
    db_FTask.action = ftask.action
    db_FTask.predecessor_successor = ftask.predecessor_successor
    db_FTask.progress = ftask.progress
    db_FTask.assigned_to = ftask.assigned_to
    db_FTask.proj_id = ftask.proj_id
    db.commit()
    db.refresh(db_FTask)
    return db_FTask

