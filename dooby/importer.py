import csv

def import_csv(session, model, filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            instance = model(**row)
            session.add(instance)
        session.commit()
