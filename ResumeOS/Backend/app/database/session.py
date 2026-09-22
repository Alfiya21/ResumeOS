from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.logger import app_logger

# ==========================================================
# SQLAlchemy Engine
# ==========================================================

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)

# ==========================================================
# Database Dependency
# ==========================================================


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.
    """

    db = SessionLocal()

    try:
        yield db

    except Exception as exc:
        app_logger.exception(
            f"Database session failed: {exc}"
        )
        db.rollback()
        raise

    finally:
        db.close()


# ==========================================================
# Database Initialization
# ==========================================================


def create_database_tables() -> None:
    """
    Create all registered database tables.
    """

    from app.database.base import Base

    Base.metadata.create_all(bind=engine)

    app_logger.info(
        "Database tables initialized successfully."
    )