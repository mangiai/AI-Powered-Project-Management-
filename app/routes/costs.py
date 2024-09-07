from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import join
from schemas.costs import CostCreateSchema, CostReadSchema, CostUpdateSchema, ResponseCostSchema, ListResponseCostSchema, CostCalculateSchema
import database.costs as tc

cost_router = APIRouter(
    prefix="/costs",
)


@cost_router.get("/", response_model=ListResponseCostSchema, summary="Get Costs")
def get_tasks(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    costs= tc.get_costs(db, skip=skip, limit=limit)

    return {"code": "success", "status": status.HTTP_200_OK, "response": [CostReadSchema.model_validate(cost.__dict__) for cost in costs]}


@cost_router.post("/", response_model=ResponseCostSchema, status_code=status.HTTP_201_CREATED)
def create_cost(cost: CostCreateSchema, db: Session = Depends(get_db)):
    db_cost = tc.create_cost(db, cost)
    returned_data = CostReadSchema.model_validate(db_cost.__dict__)

    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@cost_router.get("/{cost_id}", response_model=ResponseCostSchema)
def retrieve_cost(cost_id: int = Path(...), db: Session = Depends(get_db)):
    db_cost = tc.get_cost_by_id(db, cost_id=cost_id)
    if db_cost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="cost not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": CostReadSchema.model_validate(db_cost.__dict__)}


@cost_router.put("/{cost_id}", response_model=ResponseCostSchema)
def update_cost(cost_id: int = Path(...), cost: CostUpdateSchema = None, db: Session = Depends(get_db)):
    db_cost = tc.get_cost_by_id(db, cost_id=cost_id)
    if db_cost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="cost not found")
    returned_data = CostReadSchema.model_validate((tc.update_cost(db, cost_id=cost_id, cost=cost)).__dict__)
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@cost_router.delete("/{cost_id}", response_model=ResponseCostSchema)
def delete_cost(cost_id: int = Path(...), db: Session = Depends(get_db)):
    db_task = tc.get_cost_by_id(db, cost_id=cost_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="cost not found")
    tc.delete_cost(db, cost_id=cost_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "cost deleted"}

@cost_router.get("/calculate/{cost_id}", response_model=CostCalculateSchema)
def get_cost_by_id(cost_id: int = Path(...), db: Session = Depends(get_db)):
    db_cost = tc.get_cost_by_id(db, cost_id=cost_id)
    if db_cost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cost not found")
    
    # Calculate the cost based on the requirement
    print(type(db_cost.fixed_cost))
    if db_cost.fixed_cost is not None and db_cost.fixed_cost != 0:
        planned_cost = db_cost.fixed_cost
        actual_cost = db_cost.actual_fixed_cost
    else:
        planned_cost = db_cost.cost_per_hour * db_cost.total_hours
        actual_cost = db_cost.cost_per_hour * db_cost.actual_hours
    rlt = {
        "plannedCost": planned_cost,
        "actualCost": actual_cost
    }
    return {"code": "success", "status": status.HTTP_200_OK, "response": rlt}