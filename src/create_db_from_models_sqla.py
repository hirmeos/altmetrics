"""Create tables for PostgreSQL database from models using SQLAlchemy.

usage: python create_db_from_models_sqla.py

Dependencies:
    SQLAlchemy == 1.2.14
"""

import os

from sqlalchemy import create_engine

from models import db as Base

# ## DATABASE ##
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

PORT = '5432'

SQLALCHEMY_DATABASE_URI = (
    'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DB_USER,
        passwd=DB_PASSWORD,
        host=DB_HOST,
        port=PORT,
        db=DB_NAME,
    )
)

print(SQLALCHEMY_DATABASE_URI)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
