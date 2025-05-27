from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import importlib
from dooby.model import *

Base = get_base()
_engine = None
Session = None

def import_model_module(module_name: str):
    """
    Импортирует конкретный модуль, содержащий модели.
    Например, 'dooby.model'.
    """
    importlib.import_module(module_name)

def init_db(path=":memory:", echo=False, model_module="dooby.model"):
    """
    Инициализация базы данных.
    model_module — путь к файлу, в котором находятся все SQLAlchemy модели.
    """
    global _engine, Session
    _engine = create_engine(f"sqlite:///{path}", echo=False)
    Session = sessionmaker(bind=_engine)

    # Импортируем модели из файла
    import_model_module(model_module)

    # Создаём таблицы, если они ещё не созданы
    Base.metadata.create_all(_engine)

    return _engine

def get_session():
    if Session is None:
        raise RuntimeError("Session is not initialized. Call init_db() before using the session.")
    return Session()
