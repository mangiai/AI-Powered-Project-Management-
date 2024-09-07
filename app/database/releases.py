from sqlalchemy.orm import Session
from models.releases import Release
from schemas.releases import ReleaseCreateSchema, ReleaseUpdateSchema


def get_releases(db: Session, skip: int = 0, limit: int = 100, product_id:int = None):
    query = db.query(Release)
    if product_id:
        query = query.filter(Release.product_id == product_id)
    return query.offset(skip).limit(limit).all()


def get_release_by_id(db: Session, release_id: int):
    return db.query(Release).filter(Release.id == release_id).first()


def create_release(db: Session, release: ReleaseCreateSchema):
    db_release = Release(name=release.name,
                   description=release.description
                   , StartDate=release.StartDate, EndDate=release.EndDate,
                   release_lifecycle_id = release.release_lifecycle_id, product_id = release.product_id)
    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release


def delete_release(db: Session, release_id: int):
    db_release = db.query(Release).filter(Release.id == release_id).first()
    db.delete(db_release)
    db.commit()


def update_release(db: Session, release_id: int, release: ReleaseUpdateSchema):
    db_release = db.query(Release).filter(Release.id == release_id).first()
    db_release.name = release.name
    db_release.description = release.description
    db_release.StartDate = release.StartDate
    db_release.EndDate = release.EndDate
    db_release.release_lifecycle_id = release.release_lifecycle_id
    db_release.product_id = release.product_id
    db.commit()
    db.refresh(db_release)
    return db_release

