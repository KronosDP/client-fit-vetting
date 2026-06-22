"""
database.py — SQLAlchemy engine, session factory, and Base.

The database path defaults to a local `data/` directory but can be overridden
via the DATABASE_PATH environment variable (e.g., /data/staffinc_mvp.db for
Railway volume mounts).
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ---------------------------------------------------------------------------
# Database path configuration
# ---------------------------------------------------------------------------
_default_db_dir = Path(__file__).resolve().parent.parent / "data"
_default_db_dir.mkdir(parents=True, exist_ok=True)
_default_db_path = _default_db_dir / "staffinc_mvp.db"

DATABASE_PATH = os.getenv("DATABASE_PATH", str(_default_db_path))
# Ensure the parent directory of the database file exists (e.g. for custom volume mounts)
Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# ---------------------------------------------------------------------------
# Engine & session
# ---------------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass


# ---------------------------------------------------------------------------
# Dependency for FastAPI route injection
# ---------------------------------------------------------------------------
def get_db():
    """Yield a database session and ensure it is closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
