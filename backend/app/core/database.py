from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_settings

settings = get_settings()

# Use SQLite by default for simplicity
db_url = settings.database_url

# Override with SQLite for now if PostgreSQL fails
use_sqlite = db_url.startswith('postgres://') or db_url.startswith('postgresql://')

# Fix postgres:// -> postgresql://
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

if use_sqlite:
    # Use SQLite fallback for Render free tier issues
    db_url = "sqlite:///./agenda.db"
    print("⚠️ Using SQLite fallback instead of PostgreSQL")

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {"sslmode": "require"},
    pool_pre_ping=True,
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

sync_engine = engine  # Alias for compatibility
