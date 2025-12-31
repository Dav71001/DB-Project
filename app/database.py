from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Используем ваш реальный пароль и новый драйвер psycopg
DATABASE_URL = "postgresql+psycopg://postgres:368366@localhost/utility_payments"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()