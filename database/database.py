from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.table_model import Base  # Impor Base dan model dari file table_model.py
from dotenv import load_dotenv
import os

load_dotenv()

def initialize_db():
    engine = create_engine(os.getenv('db_engine'))
    Base.metadata.create_all(engine)  # Membuat tabel jika belum ada
    return engine
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
