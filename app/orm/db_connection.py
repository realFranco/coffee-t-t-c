"""
Connection worker for Postgres.
"""
import os
from typing import Iterator, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager


# DB Connection context.
engine = create_engine(os.environ.get('DATABASE_URL'), pool_size=25, max_overflow=5)
# metadata = MetaData(engine, schema='postgres')

# Base to instance the ORM Tables.
Base = declarative_base()
Base.metadata.create_all(engine)

local_session = sessionmaker(engine)

# DB sessions context.
def session() -> Iterator[Any]:
    try:
        s = local_session()
        yield s
    finally:
        s.close()

# Useful to create a with context.
@contextmanager
def context_session() -> Iterator[Any]:
    try:
        s = local_session()
        yield s
    finally:
        s.close()
