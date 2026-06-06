from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_PATH, ensure_directories


ensure_directories()

engine = create_engine(f"sqlite:///{DATABASE_PATH}", future=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
