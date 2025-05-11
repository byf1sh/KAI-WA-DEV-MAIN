from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    age = Column(Integer)

class JiraData(Base):
    __tablename__ = 'jira_data'
    id = Column(Integer, primary_key=True)
    case_id = Column(String(30))

class WaData(Base):
    __tablename__ = 'wa_data'
    id = Column(Integer, primary_key=True)
    case_id = Column(String(30))
    content = Column(String(255))

class EmailData(Base):
    __tablename__ = 'email_data'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    case_id = Column(String(30))
    content = Column(String(255))
