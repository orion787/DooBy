from dooby.core import init_db
from dooby.import_helper import import_from_file
from models import Partner
from sqlalchemy.orm import Session, sessionmaker

engine = init_db("partners.db")
Session = sessionmaker(bind=engine)
session = Session()


column_mapping = {
    "Тип партнера": "type",
    "Наименование партнера": "name",
    "Директор": "director",
    "Электронная почта партнера": "email",
    "Телефон партнера": "phone",
    "Рейтинг": "rating"
}

import_from_file("data/Partners_import.xlsx", Partner, session, column_mapping=column_mapping)
