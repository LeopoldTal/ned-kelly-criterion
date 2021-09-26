import os

from sqlalchemy import create_engine

user = os.getenv("DB_USER","postgres")
password = os.getenv("DB_PASSWORD","")
database_name = os.getenv("DB_NAME","postgres")
database_url = os.getenv("DB_URL","localhost")
engine = create_engine(f'postgresql://{user}@{database_url}:5432/{database_name}')


def setup():
    con = engine.connect()
    con.execute("""
    CREATE TABLE IF NOT EXISTS student (       
                    student_id SERIAL PRIMARY KEY,
                    student_name VARCHAR(255) NOT NULL)
    """)
    con.execute("""INSERT INTO student (student_name) VALUES ('Bob')""")