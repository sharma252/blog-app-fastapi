from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

# mysql - dialect, pymysql - driver
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

if not SQLALCHEMY_DATABASE_URL:
    raise Exception("DB URL is empty")

# engine = connection manager: URL picks the dialect & driver,
# connection pool defaults come from create_engine (tunable via pool_size, max_overflow, etc.)
engine = create_engine(SQLALCHEMY_DATABASE_URL)  # type: ignore

# gives a fresh db session whenever get_db is called
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# defined here as a centeral point - good when we have multiple models file
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
