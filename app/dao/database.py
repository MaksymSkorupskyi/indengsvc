import json
import os
import threading

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

thread_local = threading.local()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN")

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DB_CONN not set")


def serialize(data):
    return json.dumps(data, default=str)


def deserialize(data):
    return json.loads(data)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    json_serializer=serialize,
    json_deserializer=deserialize,
    max_overflow=10,
    pool_size=40,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(bind=engine)


def get_relativity_db_session() -> SessionLocal:
    """Retrieve or create a thread-specific database session.

    When called, it looks up a session specific to the current thread.
    If no session exists, it creates a new one. This allows each thread
    to have an independent session.

    The returned SessionLocal is meant for DB operations within the
    scope of the current thread. It should be properly closed or scoped
    to manage connections.

    Returns:
        SessionLocal: The thread-specific database session.

    Note:
        - The `SessionLocal` returned by this function is meant for database operations
          within the scope of the current thread. It should be properly closed or scoped
          using context managers to manage the database connections and resources.

    Warning:
        - Make sure to handle the `SessionLocal` correctly within the context of each thread
          to avoid potential issues with database connections and resource management.

    """
    if not hasattr(thread_local, "db_session"):
        thread_local.db_session = SessionLocal()

    return thread_local.db_session
