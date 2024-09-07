from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import get_db
from sqlalchemy.orm import Session
from schemas.stories import *
import database.stories as lc


story_router = APIRouter(
    prefix="/stories",
)


@story_router.get("/", response_model=ListResponseStorySchema)
def get_story(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, sprint_id: int = None):
    story = lc.get_stories(db, skip=skip, limit=limit, sprint_id = sprint_id)
    return {"code": "success", "status": status.HTTP_200_OK, "response": story}


@story_router.post("/", response_model=ResponseStorySchema, status_code=status.HTTP_201_CREATED)
def create_story(story: StoryCreateSchema, db: Session = Depends(get_db)):
    returned_data = StoryReadSchema.model_validate(lc.create_story(db, story))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}


@story_router.get("/{story_id}", response_model=ResponseStorySchema)
def retrieve_story(story_id: int = Path(...), db: Session = Depends(get_db)):
    db_story = lc.get_story_by_id(db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="story not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_story}


@story_router.put("/{story_id}", response_model=ResponseStorySchema)
def update_story(story_id: int = Path(...), story: StoryUpdateSchema = None, db: Session = Depends(get_db)):
    db_story = lc.get_story_by_id(db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="story not found")
    returned_data = StoryReadSchema.model_validate(lc.update_story(db, story_id=story_id, story=story))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}


@story_router.delete("/{story_id}", response_model=ResponseStorySchema)
def delete_story(story_id: int = Path(...), db: Session = Depends(get_db)):
    db_story = lc.get_story_by_id(db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="story not found")
    lc.delete_story(db, story_id=story_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "story deleted"}