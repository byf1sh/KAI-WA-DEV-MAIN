from database.database import create_session

def insert_data(session, model, **kwargs):
    new_data = model(**kwargs)
    session.add(new_data)

def prevent_duplicate_data(session, model, case_id):
    """ Mengecek apakah data sudah ada di database """
    result = session.query(model).filter(model.case_id == case_id).first()
    return result
