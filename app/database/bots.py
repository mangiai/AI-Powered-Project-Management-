from sqlalchemy.orm import Session
from models.bots import Bot
from schemas.bots import BotCreateSchema, BotUpdateSchema

def get_bots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Bot).offset(skip).limit(limit).all()

def get_bot_by_id(db: Session, bot_id: int):
    return db.query(Bot).filter(Bot.bot_id == bot_id).first()

def create_bot(db: Session, bot: BotCreateSchema):
    db_bot = Bot(bot_name=bot.bot_name, bot_description=bot.bot_description)
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

def delete_bot(db: Session, bot_id: int):
    db_bot = db.query(Bot).filter(Bot.bot_id == bot_id).first()
    db.delete(db_bot)
    db.commit()

def update_bot(db: Session, bot_id: int, bot: BotUpdateSchema):
    db_bot = db.query(Bot).filter(Bot.bot_id == bot_id).first()
    db_bot.bot_name = bot.bot_name
    db_bot.bot_description = bot.bot_description
    db.commit()
    db.refresh(db_bot)
    return db_bot
