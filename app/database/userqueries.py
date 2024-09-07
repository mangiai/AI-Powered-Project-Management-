from sqlalchemy.orm import Session
from models.userqueries import UserQuery
from schemas.userqueries import UserQueryCreateSchema, UserQueryUpdateSchema

def get_userqueries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserQuery).offset(skip).limit(limit).all()

def get_userquery_by_id(db: Session, query_id: int):
    return db.query(UserQuery).filter(UserQuery.query_id == query_id).first()

def create_userquery(db: Session, userquery: UserQueryCreateSchema):
    db_userquery = UserQuery(
        user_id=userquery.user_id,
        project_id=userquery.project_id,
        program_id=userquery.program_id,
        portfolio_id=userquery.portfolio_id,
        query_text=userquery.query_text
    )
    db.add(db_userquery)
    db.commit()
    db.refresh(db_userquery)
    return db_userquery

def delete_userquery(db: Session, query_id: int):
    db_userquery = db.query(UserQuery).filter(UserQuery.query_id == query_id).first()
    db.delete(db_userquery)
    db.commit()

def update_userquery(db: Session, query_id: int, userquery: UserQueryUpdateSchema):
    db_userquery = db.query(UserQuery).filter(UserQuery.query_id == query_id).first()
    db_userquery.user_id = userquery.user_id
    db_userquery.project_id = userquery.project_id
    db_userquery.program_id = userquery.program_id
    db_userquery.portfolio_id = userquery.portfolio_id
    db_userquery.query_text = userquery.query_text
    db.commit()
    db.refresh(db_userquery)
    return db_userquery
