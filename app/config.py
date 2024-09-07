from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
import asyncpg

POSTGRES_CONNECTION = {
    "dbname": "appdb",
    "user": "postgres",
    "password": "Stewardiq3939",
    "host": "34.134.50.75",
    "port": "5432"
}

DATABASE_URL = 'postgresql+pg8000://postgres:Stewardiq3939@34.134.50.75:5432/appdb'
DATABASE = 'postgresql://postgres:Stewardiq3939@34.134.50.75:5432/appdb'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def connect_to_db():
    return await asyncpg.connect(DATABASE)

async def close_db_connection(connection):
    await connection.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_api_key():
    return OPEN_AI_API