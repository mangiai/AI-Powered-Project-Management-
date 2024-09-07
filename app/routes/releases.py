from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.releases import ReleaseCreateSchema, ReleaseReadSchema, ReleaseUpdateSchema, ResponseReleaseSchema, ListResponseReleaseSchema
import database.releases as lc


release_router = APIRouter(
    prefix="/release",
)


@release_router.get("/", response_model=ListResponseReleaseSchema)
def get_releases(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, product_id:int = None):
    releases = lc.get_releases(db, skip=skip, limit=limit, product_id = product_id)
    return {"code": "success", "status": status.HTTP_200_OK, "response": releases}


@release_router.post("/", response_model=ResponseReleaseSchema, status_code=status.HTTP_201_CREATED)
def create_release(release: ReleaseCreateSchema, db: Session = Depends(get_db)):
    returned_data = ReleaseReadSchema.model_validate(lc.create_release(db, release))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@release_router.get("/{release_id}", response_model=ResponseReleaseSchema)
def retrieve_release(release_id: int = Path(...), db: Session = Depends(get_db)):
    db_release = lc.get_release_by_id(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="release not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_release}


@release_router.put("/{release_id}", response_model=ResponseReleaseSchema)
def update_release(release_id: int = Path(...), release: ReleaseUpdateSchema = None, db: Session = Depends(get_db)):
    db_release = lc.get_release_by_id(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="release not found")
    returned_data = ReleaseReadSchema.model_validate(lc.update_release(db, release_id=release_id, release=release))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@release_router.delete("/{release_id}", response_model=ResponseReleaseSchema)
def delete_release(release_id: int = Path(...), db: Session = Depends(get_db)):
    db_release = lc.get_release_by_id(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="release not found")
    lc.delete_release(db, release_id=release_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "release deleted"}