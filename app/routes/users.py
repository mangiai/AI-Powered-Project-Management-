from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import join
from schemas.users import UserCreateSchema, UserReadSchema, UserUpdateSchema, ResponseUserSchema, ListResponseUserSchema
import database.users as tc

user_router = APIRouter(
    prefix="/users",
)


@user_router.get("/", response_model=ListResponseUserSchema)
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    users= tc.get_users(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": users}


@user_router.post("/", response_model=ResponseUserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    returned_data = UserReadSchema.model_validate(tc.create_user(db, user))

    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@user_router.get("/{user_id}", response_model=ResponseUserSchema)
def retrieve_user(user_id: int = Path(...), db: Session = Depends(get_db)):
    db_user = tc.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_user}


@user_router.put("/{user_id}", response_model=ResponseUserSchema)
def update_user(user_id: int = Path(...), user: UserUpdateSchema = None, db: Session = Depends(get_db)):
    db_user = tc.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    returned_data = UserReadSchema.model_validate(tc.update_user(db, user_id=user_id, user=user))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@user_router.delete("/{user_id}", response_model=ResponseUserSchema)
def delete_user(user_id: int = Path(...), db: Session = Depends(get_db)):
    db_user = tc.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    tc.delete_user(db, user_id=user_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "user deleted"}