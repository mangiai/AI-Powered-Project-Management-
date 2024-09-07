from sqlalchemy.orm import Session, joinedload
from models.roadmaps import Roadmap
from datetime import datetime

# Assuming the presence of these import statements for schema validation
from schemas.roadmaps import RoadmapCreateSchema, RoadmapUpdateSchema

def get_roadmaps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Roadmap).options(joinedload(Roadmap.proj_roadmap_name)).filter(Roadmap.is_active == True).offset(skip).limit(limit).all()

def get_roadmap_by_id(db: Session, roadmap_id: int):
    return db.query(Roadmap).options(joinedload(Roadmap.proj_roadmap_name)).filter(Roadmap.id == roadmap_id).first()

def create_roadmap(db: Session, roadmap: RoadmapCreateSchema):
    # Firstly, deactivate any active roadmap for the given project, program, or portfolio
    db.query(Roadmap).filter(
        (Roadmap.project_id == roadmap.project_id) &
        (Roadmap.program_id == roadmap.program_id) &
        (Roadmap.portfolio_id == roadmap.portfolio_id),
        Roadmap.is_active == True
    ).update({"is_active": False}, synchronize_session="fetch")
    db.commit()

    # Now, create the new active roadmap
    db_Roadmap = Roadmap(
        name=roadmap.name,
        description=roadmap.description,
        project_id=roadmap.project_id,
        program_id=roadmap.program_id,
        portfolio_id=roadmap.portfolio_id,
        is_active=True  # Assuming the presence of a datetime field for when the record is created
    )
    db.add(db_Roadmap)
    db.commit()
    db.refresh(db_Roadmap)
    return db_Roadmap

def delete_roadmap(db: Session, roadmap_id: int):
    db_Roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if db_Roadmap:
        db.delete(db_Roadmap)
        db.commit()
    else:
        # Optionally, you can handle the case when the roadmap is not found
        pass

def update_roadmap(db: Session, roadmap_id: int, roadmap: RoadmapUpdateSchema):
    # Create a new roadmap instead of updating the existing one
    original_roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id, Roadmap.is_active == True).first()
    if original_roadmap:
        # Firstly, deactivate the current/old roadmap
        original_roadmap.is_active = False
        db.commit()

        # Create a new roadmap record with the updated details
        new_roadmap = Roadmap(
            name=roadmap.name,
            description=roadmap.description,
            project_id=roadmap.project_id,
            program_id=roadmap.program_id,
            portfolio_id=roadmap.portfolio_id,
            is_active=True
        )
        db.add(new_roadmap)
        db.commit()
        db.refresh(new_roadmap)
        return new_roadmap
    else:
        # Optionally, handle case when the original roadmap is not found
        return None