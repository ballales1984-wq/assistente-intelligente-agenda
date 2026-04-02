from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_settings

settings = get_settings()

# Fix postgres:// -> postgresql://
db_url = settings.database_url
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

# Use asyncpg for PostgreSQL
if 'postgresql' in db_url:
    # Convert to asyncpg format
    async_db_url = db_url.replace('postgresql://', 'postgresql+asyncpg://')
    if 'sslmode' not in db_url:
        if '?' in async_db_url:
            async_db_url += '&sslmode=require'
        else:
            async_db_url += '?sslmode=require'
    
    engine = create_async_engine(
        async_db_url,
        pool_pre_ping=True,
        echo=settings.debug
    )
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async def get_db():
        async with AsyncSessionLocal() as session:
            yield session
else:
    # SQLite fallback
    engine = create_engine(db_url, echo=settings.debug)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

Base = declarative_base()

# Sync engine for create_all (runs at startup)
if 'postgresql' in db_url:
    sync_db_url = db_url
    if 'sslmode' not in sync_db_url:
        if '?' in sync_db_url:
            sync_db_url += '&sslmode=require'
        else:
            sync_db_url += '?sslmode=require'
    sync_engine = create_engine(sync_db_url, pool_pre_ping=True)
else:
    sync_engine = engine

def get_sync_db():
    Session = sessionmaker(bind=sync_engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
