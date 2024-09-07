from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.roadmaps import RequestRoadmap, ResponseRoadmap, ListResponseRoadmap
import database.originroadmaps as lc


roadmap_router = APIRouter(
    prefix="/roadmap",
)


@roadmap_router.get("/", response_model=ListResponseRoadmap)
def get_roadmap(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    roadmap = lc.get_roadmaps(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": roadmap}


@roadmap_router.post("/", response_model=ResponseRoadmap, status_code=status.HTTP_201_CREATED)
def create_roadmap(roadmap: RequestRoadmap, db: Session = Depends(get_db)):
    lc.create_roadmap(db, roadmap)
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": roadmap}


@roadmap_router.get("/{roadmap_id}", response_model=ResponseRoadmap)
def retrieve_roadmap(roadmap_id: int = Path(...), db: Session = Depends(get_db)):
    db_roadmap = lc.get_roadmap_by_id(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="roadmap not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_roadmap}


@roadmap_router.put("/{roadmap_id}", response_model=ResponseRoadmap)
def update_roadmap(roadmap_id: int = Path(...), roadmap: RequestRoadmap = None, db: Session = Depends(get_db)):
    db_roadmap = lc.get_roadmap_by_id(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="roadmap not found")
    lc.update_roadmap(db, roadmap_id=roadmap_id, roadmap=roadmap)
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_roadmap}


@roadmap_router.delete("/{roadmap_id}", response_model=ResponseRoadmap)
def delete_roadmap(roadmap_id: int = Path(...), db: Session = Depends(get_db)):
    db_roadmap = lc.get_roadmap_by_id(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="roadmap not found")
    lc.delete_roadmap(db, roadmap_id=roadmap_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "roadmap deleted"}