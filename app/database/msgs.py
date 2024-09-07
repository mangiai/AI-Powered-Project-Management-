from sqlalchemy.orm import Session
from models.msgs import Msg
from schemas.msgs import MsgCreateSchema, MsgUpdateSchema

def get_msgs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Msg).offset(skip).limit(limit).all()

def get_msg_by_id(db: Session, msg_id: int):
    return db.query(Msg).filter(Msg.msg_id == msg_id).first()

def create_msg(db: Session, msg: MsgCreateSchema):
    db_msg = Msg(
        chat_id=msg.chat_id,
        content=msg.content,
        msg_type=msg.msg_type
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

def delete_msg(db: Session, msg_id: int):
    db_msg = db.query(Msg).filter(Msg.msg_id == msg_id).first()
    db.delete(db_msg)
    db.commit()

def update_msg(db: Session, msg_id: int, msg: MsgUpdateSchema):
    db_msg = db.query(Msg).filter(Msg.msg_id == msg_id).first()
    db_msg.chat_id = msg.chat_id
    db_msg.content = msg.content
    db_msg.msg_type = msg.msg_type
    db.commit()
    db.refresh(db_msg)
    return db_msg
