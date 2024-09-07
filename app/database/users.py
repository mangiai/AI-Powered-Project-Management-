from sqlalchemy.orm import Session
from models.users import User
from schemas.users import UserCreateSchema, UserUpdateSchema




def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreateSchema):
    db_User = User(email=user.email,
                    password=user.password, username = user.username, first_name = user.first_name, last_name = user.last_name, 
                    is_system_admin = user.is_system_admin, is_fte = user.is_fte, is_business_steward = user.is_business_steward,
                    is_resource = user.is_resource, is_onshore = user.is_onshore, access_level = user.access_level)
    db.add(db_User)
    db.commit()
    db.refresh(db_User)
    return db_User


def delete_user(db: Session, user_id: int):
    db_User = db.query(User).filter(User.id == user_id).first()
    db.delete(db_User)
    db.commit()


def update_user(db: Session, user_id: int, user: UserUpdateSchema):
    db_User = db.query(User).filter(User.id == user_id).first()
    db_User.email=user.email
    db_User.password=user.password
    db_User.username = user.username
    db_User.first_name = user.first_name
    db_User.last_name = user.last_name 
    db_User.is_system_admin = user.is_system_admin
    db_User.is_fte = user.is_fte
    db_User.is_business_steward = user.is_business_steward
    db_User.is_resource = user.is_resource
    db_User.is_onshore = user.is_onshore
    db_User.access_level = user.access_level
    db.commit()
    db.refresh(db_User)
    return db_User



