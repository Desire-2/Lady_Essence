from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Parent, Child, Appointment, Feedback
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Database configuration
DATABASE_URI = 'sqlite:///lady_essence.db'

# Initialize the database
def init_db():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
    return engine

# Create a session for database operations
def get_session():
    engine = init_db()
    Session = sessionmaker(bind=engine)
    return Session()

# Save a parent to the database
def save_parent(phone_number, name, password):
    session = get_session()
    hashed_password = generate_password_hash(password)
    parent = Parent(phone_number=phone_number, name=name, password_hash=hashed_password)
    session.add(parent)
    session.commit()

# Save a child to the database
def save_child(parent_phone, name, cycle_length, last_period_date):
    session = get_session()
    child = Child(parent_phone=parent_phone, name=name, cycle_length=cycle_length, last_period_date=last_period_date)
    session.add(child)
    session.commit()

# Fetch children for a parent
def get_children(parent_phone):
    session = get_session()
    return session.query(Child).filter_by(parent_phone=parent_phone).all()

# Update a parent's account
def update_account(phone_number, new_name):
    session = get_session()
    parent = session.query(Parent).filter_by(phone_number=phone_number).first()
    if parent:
        parent.name = new_name
        session.commit()

# Delete a parent's account
def delete_account(phone_number):
    session = get_session()
    parent = session.query(Parent).filter_by(phone_number=phone_number).first()
    if parent:
        session.delete(parent)
        session.commit()

# Delete a child
def delete_child(parent_phone, child_name):
    session = get_session()
    child = session.query(Child).filter_by(parent_phone=parent_phone, name=child_name).first()
    if child:
        session.delete(child)
        session.commit()

# Authenticate a user
def authenticate_user(phone_number, password):
    session = get_session()
    user = session.query(Parent).filter_by(phone_number=phone_number).first()
    if user and check_password_hash(user.password_hash, password):
        return True
    return False

# In database.py
def register_user(name, phone_number, password):
    session = get_session()
    hashed_password = generate_password_hash(password)
    user = Parent(name=name, phone_number=phone_number, password_hash=hashed_password)
    session.add(user)
    session.commit()

def check_password_hash(phone_number, password):
    session = get_session()
    user = session.query(Parent).filter_by(phone_number=phone_number).first()
    return check_password_hash(user.password_hash, password) if user else False

def get_user_profile(phone_number):
    session = get_session()
    user = session.query(Parent).filter_by(phone_number=phone_number).first()
    return user if user else None


def schedule_appointment(phone_number, issue):
    session = get_session()
    appointment = Appointment(
        phone_number=phone_number,
        issue=issue,
        timestamp=datetime.now()
    )
    session.add(appointment)
    session.commit()

def submit_feedback(phone_number, message):
    session = get_session()
    feedback = Feedback(
        phone_number=phone_number,
        message=message,
        timestamp=datetime.now()
    )
    session.add(feedback)
    session.commit()