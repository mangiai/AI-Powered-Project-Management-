from sqlalchemy.orm import Session
from models.stories import Story
from schemas.stories import StoryCreateSchema, StoryUpdateSchema


def get_stories(db: Session, skip: int = 0, limit: int = 100, sprint_id: int = None):
    query = db.query(Story)
    if sprint_id:
        query = query.filter(Story.sprint_id == sprint_id)
    return query.offset(skip).limit(limit).all()


def get_story_by_id(db: Session, story_id: int):
    return db.query(Story).filter(Story.id == story_id).first()

def create_story(db: Session, story: StoryCreateSchema):
    db_story = Story(type=story.type,
                   typeofstory=story.typeofstory,
                   name = story.name,
                   iwantto = story.iwantto,
                   solcan = story.solcan,
                   acceptancecriteria = story.acceptancecriteria,
                   priority = story.priority,
                   assigned_to = story.assigned,
                   is_completed=story.completed, 
                   current_status = story.current_status,
                   velocityPoints = story.velocityPoints,
                   sprint = story.sprint,
                   taskDuration = story.taskDuration,
                   resource = story.resource,
                   actualResource = story.actualResource,
                   actualStartDate = story.actualStartDate,
                   actualEndDate = story.actualEndDate,
                   plannedStartDate = story.plannedStartDate,
                   plannedEndDate = story.plannedEndDate,
                   sprint_id = story.sprint_id,
                   epic_id = story.epic_id
                   )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story


def delete_story(db: Session, story_id: int):
    db_story = db.query(Story).filter(Story.id == story_id).first()
    db.delete(db_story)
    db.commit()


def update_story(db: Session, story_id: int, story: StoryUpdateSchema):
    db_story = db.query(Story).filter(Story.id == story_id).first()
    db_story.type=story.type
    db_story.typeofstory=story.typeofstory
    db_story.name = story.name
    db_story.iwantto = story.iwantto
    db_story.solcan = story.solcan
    db_story.acceptancecriteria = story.acceptancecriteria
    db_story.priority = story.priority
    db_story.assigned_to = story.assigned
    db_story.is_completed=story.completed 
    db_story.current_status = story.current_status
    db_story.velocityPoints = story.velocityPoints
    db_story.sprint = story.sprint
    db_story.taskDuration = story.taskDuration
    db_story.resource = story.resource
    db_story.actualResource = story.actualResource
    db_story.actualStartDate = story.actualStartDate
    db_story.actualEndDate = story.actualEndDate
    db_story.plannedStartDate = story.plannedStartDate
    db_story.plannedEndDate = story.plannedEndDate
    db_story.sprint_id = story.sprint_id
    db_story.epic_id = story.epic_id
    db.commit()
    db.refresh(db_story)
    return db_story

