import pandas as pd
from sqlalchemy.orm import Session
from typing import Type
from models import Base

def import_from_file(
    file_path: str,
    model: Type[Base],
    session: Session,
    column_mapping: dict[str, str] = None,
    sheet_name: str = None
) -> int:
    ext = file_path.lower().split('.')[-1]
    if ext == 'xlsx':
        df = pd.read_excel(file_path, sheet_name=sheet_name or 0)
    elif ext == 'csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Поддерживаются только .xlsx и .csv")

    count = 0
    for i, row in df.iterrows():
        try:
            obj_data = {}
            for col in df.columns:
                model_field = column_mapping.get(col, col) if column_mapping else col
                if hasattr(model, model_field) and pd.notna(row[col]):
                    obj_data[model_field] = row[col]

            obj = model(**obj_data)
            session.add(obj)
            count += 1
        except Exception as e:
            print(f"⚠️ Строка {i+1} пропущена: {e}")

    session.commit()
    print(f"✅ Импортировано {count} объектов {model.__name__}")
    return count
