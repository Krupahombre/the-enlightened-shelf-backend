from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from src.utils.config_provider import config_provider


DATABASE_URL = 'postgresql://{username}:{password}@{host}:{port}/{db_name}'.format(
    host=config_provider.get_config_value("database", "host"),
    port=config_provider.get_config_value("database", "port"),
    db_name=config_provider.get_config_value("database", "name"),
    username=config_provider.get_config_value("database", "user"),
    password=config_provider.get_config_value("database", "password"),
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
