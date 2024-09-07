from sqlalchemy.orm import Session
from models.kpiresults import KPIResult
from schemas.kpiresults import KPIResultCreateSchema, KPIResultUpdateSchema

def get_kpiresults(db: Session, skip: int = 0, limit: int = 100):
    return db.query(KPIResult).offset(skip).limit(limit).all()

def get_kpiresult_by_id(db: Session, kpi_id: int):
    return db.query(KPIResult).filter(KPIResult.kpi_id == kpi_id).first()

def create_kpiresult(db: Session, kpiresult: KPIResultCreateSchema):
    db_kpiresult = KPIResult(
        project_id=kpiresult.project_id,
        program_id=kpiresult.program_id,
        portfolio_id=kpiresult.portfolio_id,
        cost_kpi=kpiresult.cost_kpi,
        project_kpi=kpiresult.project_kpi,
        risk_kpi=kpiresult.risk_kpi
    )
    db.add(db_kpiresult)
    db.commit()
    db.refresh(db_kpiresult)
    return db_kpiresult

def delete_kpiresult(db: Session, kpi_id: int):
    db_kpiresult = db.query(KPIResult).filter(KPIResult.kpi_id == kpi_id).first()
    db.delete(db_kpiresult)
    db.commit()

def update_kpiresult(db: Session, kpi_id: int, kpiresult: KPIResultUpdateSchema):
    db_kpiresult = db.query(KPIResult).filter(KPIResult.kpi_id == kpi_id).first()
    db_kpiresult.project_id = kpiresult.project_id
    db_kpiresult.program_id = kpiresult.program_id
    db_kpiresult.portfolio_id = kpiresult.portfolio_id
    db_kpiresult.cost_kpi = kpiresult.cost_kpi
    db_kpiresult.project_kpi = kpiresult.project_kpi
    db_kpiresult.risk_kpi = kpiresult.risk_kpi
    db.commit()
    db.refresh(db_kpiresult)
    return db_kpiresult
