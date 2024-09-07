from sqlalchemy.orm import Session
from models.costs import Cost
from schemas.costs import CostCreateSchema, CostUpdateSchema


def get_costs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cost).offset(skip).limit(limit).all()


def get_cost_by_id(db: Session, cost_id: int):
    return db.query(Cost).filter(Cost.id == cost_id).first()


def create_cost(db: Session, cost: CostCreateSchema):
    db_Cost = Cost(cost_per_hour = cost.cost_per_hour,
                    total_hours = cost.total_hours,
                    fixed_cost = cost.fixed_cost,
                    actual_hours = cost.actual_hours,
                    actual_fixed_cost = cost.actual_fixed_cost,
                    cost_ftask_id = cost.cost_ftask_id,
                    cost_user_id = cost.cost_user_id,
                    cost_story_id = cost.cost_story_id,
                    location = cost.location
                   )
    db.add(db_Cost)
    db.commit()
    db.refresh(db_Cost)
    return db_Cost


def delete_cost(db: Session, cost_id: int):
    db_Cost = db.query(Cost).filter(Cost.id == cost_id).first()
    db.delete(db_Cost)
    db.commit()


def update_cost(db: Session, cost_id: int, cost: CostUpdateSchema):
    db_Cost = db.query(Cost).filter(Cost.id == cost_id).first()
    db_Cost.cost_per_hour = cost.cost_per_hour
    db_Cost.total_hours = cost.total_hours
    db_Cost.fixed_cost = cost.fixed_cost
    db_Cost.actual_hours = cost.actual_hours
    db_Cost.actual_fixed_cost = cost.actual_fixed_cost
    db_Cost.cost_ftask_id = cost.cost_ftask_id
    db_Cost.cost_user_id = cost.cost_user_id
    db_Cost.cost_story_id = cost.cost_story_id
    db_Cost.location = cost.location
    db.commit()
    db.refresh(db_Cost)
    return db_Cost

