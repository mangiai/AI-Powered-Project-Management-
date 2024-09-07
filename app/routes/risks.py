from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import join
from schemas.risks import RiskCreateSchema, RiskReadSchema, RiskUpdateSchema, ResponseRiskSchema, ListResponseRiskSchema
import database.risks as tc

risk_router = APIRouter(
    prefix="/risks",
)


@risk_router.get("/", response_model=ListResponseRiskSchema, summary="Get Risks")
def get_risks(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, project_id: int = None):
  risks = tc.get_risks(db, skip=skip, limit=limit, project_id=project_id)
  return {"code": "success", "status": status.HTTP_200_OK, "response": risks}


@risk_router.post("/", response_model=ResponseRiskSchema, status_code=status.HTTP_201_CREATED)
def create_risk(risk: RiskCreateSchema, db: Session = Depends(get_db)):
    returned_data = RiskReadSchema.model_validate(tc.create_risk(db, risk))

    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@risk_router.get("/{risk_id}", response_model=ResponseRiskSchema)
def retrieve_risk(risk_id: int = Path(...), db: Session = Depends(get_db)):
    db_risk = tc.get_risk_by_id(db, risk_id=risk_id)
    if db_risk is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="risk not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_risk}


@risk_router.put("/{risk_id}", response_model=ResponseRiskSchema)
def update_risk(risk_id: int = Path(...), risk: RiskUpdateSchema = None, db: Session = Depends(get_db)):
    db_risk = tc.get_risk_by_id(db, risk_id=risk_id)
    if db_risk is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="risk not found")
    returned_data = RiskReadSchema.model_validate(tc.update_risk(db, risk_id=risk_id, risk=risk))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@risk_router.delete("/{risk_id}", response_model=ResponseRiskSchema)
def delete_risk(risk_id: int = Path(...), db: Session = Depends(get_db)):
    db_task = tc.get_risk_by_id(db, risk_id=risk_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="risk not found")
    tc.delete_risk(db, risk_id=risk_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "risk deleted"}