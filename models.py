"""
Database models and engine configuration for TaskFlow.
Author: Jahanzaib Muhammad
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

# Vercel's serverless functions only allow writes to /tmp — everywhere else
# is read-only at runtime. Locally (or on Railway) we just use a regular file.
if os.environ.get("VERCEL"):
    DATABASE_URL = "sqlite:////tmp/taskflow.db"
else:
    DATABASE_URL = "sqlite:///./taskflow.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TodoItem(Base):
    """Represents a single to-do item owned by the user."""
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    notes = Column(String(500), default="")
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    """Create all tables if they don't already exist."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """FastAPI dependency that yields a DB session and closes it afterwards."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
