from sqlalchemy.orm import Session
from models.chats import Chat
from schemas.chats import ChatCreateSchema, ChatUpdateSchema

def get_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Chat).offset(skip).limit(limit).all()

def get_chat_by_id(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.chat_id == chat_id).first()

def create_chat(db: Session, chat: ChatCreateSchema):
    db_chat = Chat(
        bot_id=chat.bot_id,
        user_id=chat.user_id
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def delete_chat(db: Session, chat_id: int):
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_id).first()
    db.delete(db_chat)
    db.commit()

def update_chat(db: Session, chat_id: int, chat: ChatUpdateSchema):
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_id).first()
    db_chat.bot_id = chat.bot_id
    db_chat.user_id = chat.user_id
    db.commit()
    db.refresh(db_chat)
    return db_chat
