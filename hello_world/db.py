import os
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from .orm import *

user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD', '')
database_name = os.getenv('DB_NAME', 'postgres')
database_url = os.getenv('DB_URL', 'localhost')
engine = create_engine(f'postgresql://{user}@{database_url}:5432/{database_name}')

Base.metadata.create_all(engine)
session = Session(engine)

def get_user_by_id(user_id : int) -> User:
    return session.get(User, user_id)

def get_user_by_api_key_id(api_key_id : str) -> User:
    statement = select(User).where(User.api_key_id == api_key_id)
    return session.execute(statement).one()['User']

def create_user(email_address : str = None, api_key_id : str = None) -> User:
    now = datetime.now()
    new_user = User(
        email_address = email_address,
        api_key_id = api_key_id,
        creation_date = now,
        update_date = now
    )
    
    session.add(new_user)
    session.commit()
    
    return new_user

# TODO: update user

def get_experiment_by_id(experiment_id : int) -> Experiment:
    return session.get(Experiment, experiment_id)

def create_experiment(name: str, user_id: int) -> Experiment:
    now = datetime.now()
    new_experiment = Experiment(
        name = name,
        user_id = user_id,
        creation_date = now,
        update_date = now
    )
    
    session.add(new_experiment)
    session.commit()
    
    return new_experiment

def get_variant_by_id(variant_id : int) -> Variant:
    with Session(engine) as session:
        with session.begin():
            return session.get(Variant, variant_id)

def create_variant(name: str, experiment_id: int) -> Variant:
    now = datetime.now()
    new_variant = Variant(
        name = name,
        experiment_id = experiment_id,
        nb_successes = 0,
        nb_failures = 0,
        creation_date = now,
        update_date = now
    )
    
    session.add(new_variant)
    session.commit()
    
    return new_variant

# TODO: record success/failure for variant (must be atomic!)
