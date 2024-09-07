from sqlalchemy.orm import Session
from models.generatedsqls import GeneratedSql
from schemas.generatedsqls import GeneratedSqlCreateSchema, GeneratedSqlUpdateSchema

def get_generatedsqls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(GeneratedSql).offset(skip).limit(limit).all()

def get_generatedsql_by_id(db: Session, sql_id: int):
    return db.query(GeneratedSql).filter(GeneratedSql.sql_id == sql_id).first()

def create_generatedsql(db: Session, generatedsql: GeneratedSqlCreateSchema):
    db_generatedsql = GeneratedSql(
        query_id=generatedsql.query_id,
        sql_text=generatedsql.sql_text
    )
    db.add(db_generatedsql)
    db.commit()
    db.refresh(db_generatedsql)
    return db_generatedsql

def delete_generatedsql(db: Session, sql_id: int):
    db_generatedsql = db.query(GeneratedSql).filter(GeneratedSql.sql_id == sql_id).first()
    db.delete(db_generatedsql)
    db.commit()

def update_generatedsql(db: Session, sql_id: int, generatedsql: GeneratedSqlUpdateSchema):
    db_generatedsql = db.query(GeneratedSql).filter(GeneratedSql.sql_id == sql_id).first()
    db_generatedsql.query_id = generatedsql.query_id
    db_generatedsql.sql_text = generatedsql.sql_text
    db.commit()
    db.refresh(db_generatedsql)
    return db_generatedsql
