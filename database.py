"""Acts as main interface with database, calling and setting data"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

env_loaded_db = load_dotenv()
if not env_loaded_db:
    print("***NO ENVIRONMENT VARIABLE LOADED IN DATABASE, ABNORMAL RESULTS MAY FOLLOW***")

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Expected format: "
        "postgresql://<user>:<password>@<host>/<dbname>"
    )

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Fastapi dependency that yields a db session and always closes it"""
    db : Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

