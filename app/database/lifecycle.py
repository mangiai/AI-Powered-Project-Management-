from sqlalchemy.orm import Session
from models.lifecycle import Lifecycle
from schemas.lifecycle import LifecycleSchema



def get_lifecycle(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Lifecycle).offset(skip).limit(limit).all()


def get_lifecycle_by_id(db: Session, lifecycle_id: int):
    return db.query(Lifecycle).filter(Lifecycle.id == lifecycle_id).first()


def create_lifecycle(db: Session, lifecycle: LifecycleSchema):
    db_lifecycle = Lifecycle(phase=lifecycle.phase,
                   description=lifecycle.description)
    db.add(db_lifecycle)
    db.commit()
    db.refresh(db_lifecycle)
    return db_lifecycle


def delete_lifecycle(db: Session, lifecycle_id: int):
    db_lifecycle = db.query(Lifecycle).filter(Lifecycle.id == lifecycle_id).first()
    db.delete(db_lifecycle)
    db.commit()


def update_lifecycle(db: Session, lifecycle_id: int, lifecycle: LifecycleSchema):
    db_lifecycle = db.query(Lifecycle).filter(Lifecycle.id == lifecycle_id).first()
    db_lifecycle.phase = lifecycle.phase
    db_lifecycle.description = lifecycle.description
    db.commit()
    db.refresh(db_lifecycle)
    return db_lifecycle