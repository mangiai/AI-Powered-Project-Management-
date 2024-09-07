from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import join
from schemas.roadmaps import RoadmapCreateSchema, RoadmapReadSchema, RoadmapUpdateSchema, ResponseRoadmapSchema, ListResponseRoadmapSchema, RoadmapBaseReadSchema, ResponseRoadmapBaseSchema
import database.roadmaps as tc

roadmap_router = APIRouter(
    prefix="/roadmaps",
)


@roadmap_router.get("/", response_model=ListResponseRoadmapSchema, summary="Get Roadmaps")
def get_roadmaps(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    roadmaps= tc.get_roadmaps(db, skip=skip, limit=limit)
    return {
        "code": "success",
        "status": status.HTTP_200_OK,
        "response": [RoadmapReadSchema.model_validate(roadmap) for roadmap in roadmaps]
    }


@roadmap_router.post("/", response_model=ResponseRoadmapBaseSchema, status_code=status.HTTP_201_CREATED)
def create_roadmap(roadmap: RoadmapCreateSchema, db: Session = Depends(get_db)):
    tmp= tc.create_roadmap(db, roadmap)
    print(tmp.__dict__)
    returned_data = RoadmapBaseReadSchema.model_validate(tmp)

    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@roadmap_router.get("/{roadmap_id}", response_model=ResponseRoadmapSchema)
def retrieve_roadmap(roadmap_id: int = Path(...), db: Session = Depends(get_db)):
    db_roadmap = tc.get_roadmap_by_id(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="roadmap not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": RoadmapReadSchema.model_validate(db_roadmap)}


@roadmap_router.put("/{roadmap_id}", response_model=ResponseRoadmapSchema)
def update_roadmap(roadmap_id: int = Path(...), roadmap: RoadmapUpdateSchema = None, db: Session = Depends(get_db)):
    db_roadmap = tc.get_roadmap_by_id(db, roadmap_id=roadmap_id)
    if db_roadmap is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="roadmap not found")
    returned_data = RoadmapReadSchema.model_validate(tc.update_roadmap(db, roadmap_id=roadmap_id, roadmap=roadmap))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@roadmap_router.delete("/{roadmap_id}", response_model=ResponseRoadmapSchema)
def delete_roadmap(roadmap_id: int = Path(...), db: Session = Depends(get_db)):
    db_task = tc.get_roadmap_by_id(db, roadmap_id=roadmap_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="roadmap not found")
    tc.delete_roadmap(db, roadmap_id=roadmap_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "roadmap deleted"}