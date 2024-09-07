from fastapi import APIRouter, Depends, HTTPException, status, Path
from config import engine, connect_to_db, close_db_connection, SessionLocal, POSTGRES_CONNECTION, get_db
from sqlalchemy.orm import Session, joinedload
from schemas.bots import BotCreateSchema, BotReadSchema, BotUpdateSchema, ResponseBotSchema, ListResponseBotSchema
import database.bots as tc

bot_router = APIRouter(
    prefix="/bots",
)

@bot_router.get("/", response_model=ListResponseBotSchema)
def get_bots(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    bots = tc.get_bots(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": bots}

@bot_router.post("/", response_model=ResponseBotSchema, status_code=status.HTTP_201_CREATED)
def create_bot(bot: BotCreateSchema, db: Session = Depends(get_db)):
    returned_data = BotReadSchema.model_validate(tc.create_bot(db, bot))
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": returned_data}

@bot_router.get("/{bot_id}", response_model=ResponseBotSchema)
def retrieve_bot(bot_id: int = Path(...), db: Session = Depends(get_db)):
    db_bot = tc.get_bot_by_id(db, bot_id=bot_id)
    if db_bot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bot not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_bot}

@bot_router.put("/{bot_id}", response_model=ResponseBotSchema)
def update_bot(bot_id: int = Path(...), bot: BotUpdateSchema = None, db: Session = Depends(get_db)):
    db_bot = tc.get_bot_by_id(db, bot_id=bot_id)
    if db_bot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bot not found")
    returned_data = BotReadSchema.model_validate(tc.update_bot(db, bot_id=bot_id, bot=bot))
    return {"code": "success", "status": status.HTTP_200_OK, "response": returned_data}

@bot_router.delete("/{bot_id}", response_model=ResponseBotSchema)
def delete_bot(bot_id: int = Path(...), db: Session = Depends(get_db)):
    db_bot = tc.get_bot_by_id(db, bot_id=bot_id)
    if db_bot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bot not found")
    tc.delete_bot(db, bot_id=bot_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "Bot deleted"}
