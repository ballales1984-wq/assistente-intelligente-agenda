import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get DATABASE_URL from environment
database_url = os.environ.get('DATABASE_URL', 'sqlite:///./agenda.db')

# Fix postgres:// -> postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

# Add SSL mode for Render PostgreSQL
if 'render.com' in database_url:
    if '?' in database_url:
        if 'sslmode' not in database_url:
            database_url += '&sslmode=require'
    else:
        database_url += '?sslmode=require'
    print(f"🔗 Connecting to: {database_url[:50]}...")

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"},
    pool_size=1,
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

sync_engine = engine
