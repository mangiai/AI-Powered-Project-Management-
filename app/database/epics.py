from sqlalchemy.orm import Session
from models.epics import Epic
from schemas.epics import EpicCreateSchema, EpicUpdateSchema


def get_epics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Epic).offset(skip).limit(limit).all()


def get_epic_by_id(db: Session, epic_id: int):
    return db.query(Epic).filter(Epic.id == epic_id).first()


def create_epic(db: Session, epic: EpicCreateSchema):
    db_epic = Epic(themename=epic.themename)
    db.add(db_epic)
    db.commit()
    db.refresh(db_epic)
    return db_epic


def delete_epic(db: Session, epic_id: int):
    db_epic = db.query(Epic).filter(Epic.id == epic_id).first()
    db.delete(db_epic)
    db.commit()


def update_epic(db: Session, epic_id: int, epic: EpicUpdateSchema):
    db_epic = db.query(Epic).filter(Epic.id == epic_id).first()
    db_epic.themename = epic.themename
    db.commit()
    db.refresh(db_epic)
    return db_epic

