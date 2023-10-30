from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declared_attr

import settings

SQLALCHEMY_DATABASE_URL = settings.settings.url_db

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


Base = declarative_base(cls=BaseModel)


class AuthorizationCode(Base):
    authorization_code = Column(String(766), unique=True, index=True, )
    client_id = Column(String(60), index=True, )
    redirect_url = Column(String(1024))
    expiration_date = Column(DateTime)
    code_challenge = Column(String(1024), index=True)


Base.metadata.create_all(engine)
