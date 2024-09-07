from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from schemas.uploadedcsvs import UploadedCSVCreateSchema, UploadedCSVReadSchema, UploadedCSVUpdateSchema, ResponseUploadedCSVSchema, ListResponseUploadedCSVSchema
import database.uploadedcsvs as tc

uploadedcsv_router = APIRouter(
    prefix="/uploadedcsvs",
)

@uploadedcsv_router.get("/", response_model=ListResponseUploadedCSVSchema)
def get_uploadedcsvs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    uploadedcsvs = tc.get_uploadedcsvs(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": uploadedcsvs}

@uploadedcsv_router.post("/", response_model=ResponseUploadedCSVSchema, status_code=status.HTTP_201_CREATED)
def create_uploadedcsv(uploadedcsv: UploadedCSVCreateSchema, db: Session = Depends(get_db)):
    returned_data = UploadedCSVReadSchema.model_validate(tc.create_uploadedcsv(db, uploadedcsv))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}

@uploadedcsv_router.get("/{csv_id}", response_model=ResponseUploadedCSVSchema)
def retrieve_uploadedcsv(csv_id: int = Path(...), db: Session = Depends(get_db)):
    db_uploadedcsv = tc.get_uploadedcsv_by_id(db, csv_id=csv_id)
    if db_uploadedcsv is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Uploaded CSV not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_uploadedcsv}

@uploadedcsv_router.put("/{csv_id}", response_model=ResponseUploadedCSVSchema)
def update_uploadedcsv(csv_id: int = Path(...), uploadedcsv: UploadedCSVUpdateSchema = None, db: Session = Depends(get_db)):
    db_uploadedcsv = tc.get_uploadedcsv_by_id(db, csv_id=csv_id)
    if db_uploadedcsv is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Uploaded CSV not found")
    returned_data = UploadedCSVReadSchema.model_validate(tc.update_uploadedcsv(db, csv_id=csv_id, uploadedcsv=uploadedcsv))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}

@uploadedcsv_router.delete("/{csv_id}", response_model=ResponseUploadedCSVSchema)
def delete_uploadedcsv(csv_id: int = Path(...), db: Session = Depends(get_db)):
    db_uploadedcsv = tc.get_uploadedcsv_by_id(db, csv_id=csv_id)
    if db_uploadedcsv is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Uploaded CSV not found")
    tc.delete_uploadedcsv(db, csv_id=csv_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "Uploaded CSV deleted"}
