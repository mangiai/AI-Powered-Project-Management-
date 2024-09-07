from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from schemas.userqueries import UserQueryCreateSchema, UserQueryReadSchema, UserQueryUpdateSchema, ResponseUserQuerySchema, ListResponseUserQuerySchema
import database.userqueries as tc

userquery_router = APIRouter(
    prefix="/userqueries",
)

@userquery_router.get("/", response_model=ListResponseUserQuerySchema)
def get_userqueries(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    userqueries = tc.get_userqueries(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": userqueries}

@userquery_router.post("/", response_model=ResponseUserQuerySchema, status_code=status.HTTP_201_CREATED)
def create_userquery(userquery: UserQueryCreateSchema, db: Session = Depends(get_db)):
    returned_data = UserQueryReadSchema.model_validate(tc.create_userquery(db, userquery))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}

@userquery_router.get("/{query_id}", response_model=ResponseUserQuerySchema)
def retrieve_userquery(query_id: int = Path(...), db: Session = Depends(get_db)):
    db_userquery = tc.get_userquery_by_id(db, query_id=query_id)
    if db_userquery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserQuery not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_userquery}

@userquery_router.put("/{query_id}", response_model=ResponseUserQuerySchema)
def update_userquery(query_id: int = Path(...), userquery: UserQueryUpdateSchema = None, db: Session = Depends(get_db)):
    db_userquery = tc.get_userquery_by_id(db, query_id=query_id)
    if db_userquery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserQuery not found")
    returned_data = UserQueryReadSchema.model_validate(tc.update_userquery(db, query_id=query_id, userquery=userquery))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}

@userquery_router.delete("/{query_id}", response_model=ResponseUserQuerySchema)
def delete_userquery(query_id: int = Path(...), db: Session = Depends(get_db)):
    db_userquery = tc.get_userquery_by_id(db, query_id=query_id)
    if db_userquery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserQuery not found")
    tc.delete_userquery(db, query_id=query_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "UserQuery deleted"}
