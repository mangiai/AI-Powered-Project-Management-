from sqlalchemy.orm import Session
from models.risks import Risk
from datetime import datetime
# Assuming the presence of these import statements for schema validation
from schemas.risks import RiskCreateSchema, RiskUpdateSchema

def get_risks(db: Session, skip: int = 0, limit: int = 100, project_id: int = None):
  query = db.query(Risk)
  if project_id:
    query = query.filter(Risk.risk_proj_id == project_id)
  return query.offset(skip).limit(limit).all()

def get_risk_by_id(db: Session, risk_id: int):
    return db.query(Risk).filter(Risk.id == risk_id).first()

def create_risk(db: Session, risk: RiskCreateSchema):
    # Firstly, deactivate any active risk for the given project, program, or portfolio
    db.query(Risk).filter(
        (Risk.risk_proj_id == risk.risk_proj_id) &
        (Risk.risk_prog_id == risk.risk_prog_id) &
        (Risk.risk_port_id == risk.risk_port_id),
        Risk.is_active == True
    ).update({"is_active": False}, synchronize_session="fetch")
    db.commit()

    # Now, create the new active risk
    db_Risk = Risk(
        type = risk.type,
        name=risk.name,
        description=risk.description,
        mitigation = risk.mitigation,
        assigned_to = risk.assigned_to,
        is_completed = risk.is_completed,
        risk_impact = risk.risk_impact,
        risk_probablitly = risk.risk_probablitly,
        DueDate = risk.DueDate,

        risk_proj_id=risk.risk_proj_id,
        risk_prog_id=risk.risk_prog_id,
        risk_port_id=risk.risk_port_id,
        is_active=True  # Assuming the presence of a datetime field for when the record is created
    )
    db.add(db_Risk)
    db.commit()
    db.refresh(db_Risk)
    return db_Risk

def delete_risk(db: Session, risk_id: int):
    db_Risk = db.query(Risk).filter(Risk.id == risk_id).first()
    if db_Risk:
        db.delete(db_Risk)
        db.commit()
    else:
        # Optionally, you can handle the case when the risk is not found
        pass

def update_risk(db: Session, risk_id: int, risk: RiskUpdateSchema):
    # Create a new risk instead of updating the existing one
    original_risk = db.query(Risk).filter(Risk.id == risk_id, Risk.is_active == True).first()
    if original_risk:
        # Firstly, deactivate the current/old risk
        original_risk.is_active = False
        db.commit()

        # Create a new risk record with the updated details
        new_risk = Risk(
            type = risk.type,
            name=risk.name,
            description=risk.description,
            mitigation = risk.mitigation,
            assigned_to = risk.assigned_to,
            risk_impact = risk.risk_impact,
            risk_probablitly = risk.risk_probablitly,
            is_completed = risk.is_completed,
            DueDate = risk.DueDate,
            
            risk_proj_id=risk.risk_proj_id,
            risk_prog_id=risk.risk_prog_id,
            risk_port_id=risk.risk_port_id,
            is_active=True  # Assuming the presence of a datetime field for when the record is created
        )
        db.add(new_risk)
        db.commit()
        db.refresh(new_risk)
        return new_risk
    else:
        # Optionally, handle case when the original risk is not found
        return None