from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
_engine = None
Session = None

def init_db(path=":memory:"):
    global _engine, Session
    _engine = create_engine(f"sqlite:///{path}", echo=False)
    Session = sessionmaker(bind=_engine)

    #Создание всех таблиц моделей при необходимости
    Base.metadata.create_all(_engine)

    return _engine

def get_session():
    if Session is None:
        raise RuntimeError("Session is not initialized. Call init_db() before using the session.")
    return Session()
