from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

#devuelve la sesión de la bd
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()