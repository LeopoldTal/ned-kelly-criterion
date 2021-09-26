import os
from sqlalchemy import create_engine
from .orm import *

user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "")
database_name = os.getenv("DB_NAME", "postgres")
database_url = os.getenv("DB_URL", "localhost")
engine = create_engine(f'postgresql://{user}@{database_url}:5432/{database_name}')

def setup():
    con = engine.connect()
    Base.metadata.create_all(engine)
    mytest = con.execute('SELECT * FROM experiments')
    print(mytest)
