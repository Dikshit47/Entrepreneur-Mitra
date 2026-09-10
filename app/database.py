"""SQLAlchemy Database Engine, Session Maker, and Base Declarative Model."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Resolve database URL (prefer SUPABASE_DATABASE_URL if configured)
raw_db_url = (settings.SUPABASE_DATABASE_URL or settings.DATABASE_URL).strip()
if raw_db_url.startswith("postgres://"):
    raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)

connect_args = {}
engine_kwargs = {"echo": False}

if raw_db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    # Supabase PostgreSQL connection pool settings
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = getattr(settings, "DB_POOL_SIZE", 10)
    engine_kwargs["max_overflow"] = getattr(settings, "DB_MAX_OVERFLOW", 20)
    engine_kwargs["pool_timeout"] = getattr(settings, "DB_POOL_TIMEOUT", 30)

engine = create_engine(
    raw_db_url,
    connect_args=connect_args,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_active_database_type() -> str:
    """Returns 'sqlite' or 'postgresql' based on active engine."""
    return "sqlite" if raw_db_url.startswith("sqlite") else "postgresql"


def get_db():
    """Dependency for providing a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
