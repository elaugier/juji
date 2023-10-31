from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime, String, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declared_attr

import conf

SQLALCHEMY_DATABASE_URL = conf.settings.url_db

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


class Tag(Base):
    label = Column(String(30), unique=True, index=True)
    type = Column(Enum("system", "category", "user", "event"))
    enable = Column(Boolean(), default=True)
    start_at = Column(DateTime)
    end_at = Column(DateTime)


class Section(Base):
    name = Column(String(30), unique=True, index=True)
    shortname = Column(String(10), unique=True, index=True)


class User(Base):
    firstname = Column(String(255))
    lastname = Column(String(255))


Base.metadata.create_all(engine)
