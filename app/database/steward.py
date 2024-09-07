from sqlalchemy.orm import Session
from models.steward import Steward
from schemas.steward import StewardSchema


def get_steward(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Steward).offset(skip).limit(limit).all()


def get_steward_by_id(db: Session, steward_id: int):
    return db.query(Steward.filter(Steward.id == steward_id).first())

def create_steward(db: Session, steward: StewardSchema):
    db_steward = Steward(asset_name=steward.asset_name, asset_type=steward.asset_type, asset_stage=steward.asset_stage
                        , desription=steward.description, calculation_method=steward.calculation_method
                        , calculation_value=steward.calculation_value, sor=steward.sor, dashboard_name=steward.dashboard_name
                        ,business_steward_name=steward.business_steward_name, it_custodian_name=steward.it_custodian_name,
                        value_statement=steward.value_statement, project_rank=steward.project_name)
    db.add(db_steward)
    db.commit()
    db.refresh(db_steward)
    return db_steward


def delete_steward(db: Session, steward_id: int):
    db_steward = db.query(Steward).filter(Steward.id == steward_id).first()
    db.delete(db_steward)
    db.commit()


def update_steward(db: Session, steward_id: int, steward: StewardSchema):
    db_steward = db.query(Steward).filter(Steward.id == steward_id).first()
    db_steward.asset_name = steward.asset_name
    db_steward.asset_type = steward.asset_type
    db_steward.asset_stage = steward.asset_stage
    db_steward.desription = steward.description 
    db_steward.calculation_method = steward.calculation_method
    db_steward.calculation_value = steward.calculation_value
    db_steward.sor = steward.sor
    db_steward.dashboard_name = steward.dashboard_name
    db_steward.business_steward_name = steward.business_steward_name 
    db_steward.it_custodian_name = steward.it_custodian_name
    db_steward.value_statement = steward.value_statement
    db_steward.project_rank = steward.project_name
    db.commit()
    db.refresh(db_steward)
    return db_steward

