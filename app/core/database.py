from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carga variables del .env
load_dotenv()

# Lee la URL de la BD desde el .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unicert.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Sesion para interactuar con db
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()