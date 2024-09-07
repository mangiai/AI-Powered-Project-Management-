from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from schemas.kpiresults import KPIResultCreateSchema, KPIResultReadSchema, KPIResultUpdateSchema, ResponseKPIResultSchema, ListResponseKPIResultSchema
import database.kpiresults as tc

kpiresult_router = APIRouter(
    prefix="/kpiresults",
)

@kpiresult_router.get("/", response_model=ListResponseKPIResultSchema)
def get_kpiresults(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    kpiresults = tc.get_kpiresults(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": kpiresults}

@kpiresult_router.post("/", response_model=ResponseKPIResultSchema, status_code=status.HTTP_201_CREATED)
def create_kpiresult(kpiresult: KPIResultCreateSchema, db: Session = Depends(get_db)):
    returned_data = KPIResultReadSchema.model_validate(tc.create_kpiresult(db, kpiresult))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}

@kpiresult_router.get("/{kpi_id}", response_model=ResponseKPIResultSchema)
def retrieve_kpiresult(kpi_id: int = Path(...), db: Session = Depends(get_db)):
    db_kpiresult = tc.get_kpiresult_by_id(db, kpi_id=kpi_id)
    if db_kpiresult is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KPI Result not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_kpiresult}

@kpiresult_router.put("/{kpi_id}", response_model=ResponseKPIResultSchema)
def update_kpiresult(kpi_id: int = Path(...), kpiresult: KPIResultUpdateSchema = None, db: Session = Depends(get_db)):
    db_kpiresult = tc.get_kpiresult_by_id(db, kpi_id=kpi_id)
    if db_kpiresult is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KPI Result not found")
    returned_data = KPIResultReadSchema.model_validate(tc.update_kpiresult(db, kpi_id=kpi_id, kpiresult=kpiresult))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}

@kpiresult_router.delete("/{kpi_id}", response_model=ResponseKPIResultSchema)
def delete_kpiresult(kpi_id: int = Path(...), db: Session = Depends(get_db)):
    db_kpiresult = tc.get_kpiresult_by_id(db, kpi_id=kpi_id)
    if db_kpiresult is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KPI Result not found")
    tc.delete_kpiresult(db, kpi_id=kpi_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "KPI Result deleted"}
