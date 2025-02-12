from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True)
    name = Column(String)
    password_hash = Column(String)

class Child(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    parent_phone = Column(String)
    name = Column(String)
    cycle_length = Column(Integer)
    last_period_date = Column(Date)

# In models.py
class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String)
    issue = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)