from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 환경 변수에서 가져오도록 (기본은 SQLite)
DATABASE_URL = "sqlite:///./calendar.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite 용
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

