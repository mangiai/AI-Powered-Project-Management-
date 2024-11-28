from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
import asyncpg

POSTGRES_CONNECTION = {
    "dbname": "your-db",
    "user": "your-user",
    "password": "your-pass",
    "host": "your-host",
    "port": "5432"
}

DATABASE_URL = 'DATABASE_URI'
DATABASE = 'DB'

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
