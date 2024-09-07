from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from schemas.generatedsqls import GeneratedSqlCreateSchema, GeneratedSqlReadSchema, GeneratedSqlUpdateSchema, ResponseGeneratedSqlSchema, ListResponseGeneratedSqlSchema
import database.generatedsqls as tc

generatedsql_router = APIRouter(
    prefix="/generatedsqls",
)

@generatedsql_router.get("/", response_model=ListResponseGeneratedSqlSchema)
def get_generatedsqls(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    generatedsqls = tc.get_generatedsqls(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": generatedsqls}

@generatedsql_router.post("/", response_model=ResponseGeneratedSqlSchema, status_code=status.HTTP_201_CREATED)
def create_generatedsql(generatedsql: GeneratedSqlCreateSchema, db: Session = Depends(get_db)):
    returned_data = GeneratedSqlReadSchema.model_validate(tc.create_generatedsql(db, generatedsql))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}

@generatedsql_router.get("/{sql_id}", response_model=ResponseGeneratedSqlSchema)
def retrieve_generatedsql(sql_id: int = Path(...), db: Session = Depends(get_db)):
    db_generatedsql = tc.get_generatedsql_by_id(db, sql_id=sql_id)
    if db_generatedsql is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generated SQL not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_generatedsql}

@generatedsql_router.put("/{sql_id}", response_model=ResponseGeneratedSqlSchema)
def update_generatedsql(sql_id: int = Path(...), generatedsql: GeneratedSqlUpdateSchema = None, db: Session = Depends(get_db)):
    db_generatedsql = tc.get_generatedsql_by_id(db, sql_id=sql_id)
    if db_generatedsql is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generated SQL not found")
    returned_data = GeneratedSqlReadSchema.model_validate(tc.update_generatedsql(db, sql_id=sql_id, generatedsql=generatedsql))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}

@generatedsql_router.delete("/{sql_id}", response_model=ResponseGeneratedSqlSchema)
def delete_generatedsql(sql_id: int = Path(...), db: Session = Depends(get_db)):
    db_generatedsql = tc.get_generatedsql_by_id(db, sql_id=sql_id)
    if db_generatedsql is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generated SQL not found")
    tc.delete_generatedsql(db, sql_id=sql_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "Generated SQL deleted"}
