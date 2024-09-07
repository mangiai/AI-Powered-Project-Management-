from sqlalchemy.orm import Session
from models.originroadmaps import Roadmap
from schemas.originroadmaps import RoadmapSchema


def get_roadmaps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Roadmap).offset(skip).limit(limit).all()


def get_roadmap_by_id(db: Session, roadmap_id: int):
    return db.query(Roadmap.filter(Roadmap.id == roadmap_id).first())

def create_roadmap(db: Session, roadmap: RoadmapSchema):
    db_roadmap = Roadmap(name=roadmap.name, description=roadmap.description)
    db.add(db_roadmap)
    db.commit()
    db.refresh(db_roadmap)
    return db_roadmap


def delete_roadmap(db: Session, roadmap_id: int):
    db_roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    db.delete(db_roadmap)
    db.commit()


def update_roadmap(db: Session, roadmap_id: int, roadmap: RoadmapSchema):
    db_roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    db_roadmap.name = roadmap.name
    db_roadmap.description = roadmap.description
    db.commit()
    db.refresh(db_roadmap)
    return db_roadmap

