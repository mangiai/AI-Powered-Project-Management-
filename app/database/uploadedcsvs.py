from sqlalchemy.orm import Session
from models.uploadedcsvs import UploadedCSV
from schemas.uploadedcsvs import UploadedCSVCreateSchema, UploadedCSVUpdateSchema

def get_uploadedcsvs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UploadedCSV).offset(skip).limit(limit).all()

def get_uploadedcsv_by_id(db: Session, csv_id: int):
    return db.query(UploadedCSV).filter(UploadedCSV.csv_id == csv_id).first()

def create_uploadedcsv(db: Session, uploadedcsv: UploadedCSVCreateSchema):
    db_uploadedcsv = UploadedCSV(
        user_id=uploadedcsv.user_id,
        project_id=uploadedcsv.project_id,
        program_id=uploadedcsv.program_id,
        portfolio_id=uploadedcsv.portfolio_id,
        file_path=uploadedcsv.file_path
    )
    db.add(db_uploadedcsv)
    db.commit()
    db.refresh(db_uploadedcsv)
    return db_uploadedcsv

def delete_uploadedcsv(db: Session, csv_id: int):
    db_uploadedcsv = db.query(UploadedCSV).filter(UploadedCSV.csv_id == csv_id).first()
    db.delete(db_uploadedcsv)
    db.commit()

def update_uploadedcsv(db: Session, csv_id: int, uploadedcsv: UploadedCSVUpdateSchema):
    db_uploadedcsv = db.query(UploadedCSV).filter(UploadedCSV.csv_id == csv_id).first()
    db_uploadedcsv.user_id = uploadedcsv.user_id
    db_uploadedcsv.project_id = uploadedcsv.project_id
    db_uploadedcsv.program_id = uploadedcsv.program_id
    db_uploadedcsv.portfolio_id = uploadedcsv.portfolio_id
    db_uploadedcsv.file_path = uploadedcsv.file_path
    db.commit()
    db.refresh(db_uploadedcsv)
    return db_uploadedcsv
