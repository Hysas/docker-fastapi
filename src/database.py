from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from . import config


NODE_ENV = config.settings.NODE_ENV
DB_HOST = config.settings.DB_HOST
DB_PORT = config.settings.DB_PORT
DB_USER = config.settings.DB_USER
DB_PASSWORD = config.settings.DB_PASSWORD
DB_NAME = config.settings.DB_NAME

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()