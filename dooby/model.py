from sqlalchemy.orm import declarative_base

Base = declarative_base()

def get_base():
    return Base
