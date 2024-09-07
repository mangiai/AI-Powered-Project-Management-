from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from schemas.chats import ChatCreateSchema, ChatReadSchema, ChatUpdateSchema, ResponseChatSchema, ListResponseChatSchema
import database.chats as tc

chat_router = APIRouter(
    prefix="/chats",
)

@chat_router.get("/", response_model=ListResponseChatSchema)
def get_chats(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    chats = tc.get_chats(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": chats}

@chat_router.post("/", response_model=ResponseChatSchema, status_code=status.HTTP_201_CREATED)
def create_chat(chat: ChatCreateSchema, db: Session = Depends(get_db)):
    returned_data = ChatReadSchema.model_validate(tc.create_chat(db, chat))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}

@chat_router.get("/{chat_id}", response_model=ResponseChatSchema)
def retrieve_chat(chat_id: int = Path(...), db: Session = Depends(get_db)):
    db_chat = tc.get_chat_by_id(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_chat}

@chat_router.put("/{chat_id}", response_model=ResponseChatSchema)
def update_chat(chat_id: int = Path(...), chat: ChatUpdateSchema = None, db: Session = Depends(get_db)):
    db_chat = tc.get_chat_by_id(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    returned_data = ChatReadSchema.model_validate(tc.update_chat(db, chat_id=chat_id, chat=chat))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}

@chat_router.delete("/{chat_id}", response_model=ResponseChatSchema)
def delete_chat(chat_id: int = Path(...), db: Session = Depends(get_db)):
    db_chat = tc.get_chat_by_id(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    tc.delete_chat(db, chat_id=chat_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "Chat deleted"}
