from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Generator
import re


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    database_url: str = "postgresql://postgres:postgres@localhost:5432/app"


settings = Settings()


def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    # Parse database name from URL
    match = re.search(r'/([^/]+)$', settings.database_url)
    if not match:
        return

    db_name = match.group(1)

    # Create URL for postgres database (always exists)
    postgres_url = settings.database_url.rsplit('/', 1)[0] + '/postgres'

    try:
        # Try to connect to target database
        temp_engine = create_engine(settings.database_url)
        with temp_engine.connect():
            pass
        temp_engine.dispose()
    except OperationalError as e:
        # If database doesn't exist, create it
        if 'database' in str(e) and 'does not exist' in str(e):
            print(f"Database '{db_name}' does not exist. Creating...")

            # Connect to postgres database
            postgres_engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")
            with postgres_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
            postgres_engine.dispose()

            print(f"Database '{db_name}' created successfully!")
        else:
            raise


# Create database if needed
create_database_if_not_exists()

# Create engine and session
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    from lib.models import Base
    Base.metadata.create_all(bind=engine)
