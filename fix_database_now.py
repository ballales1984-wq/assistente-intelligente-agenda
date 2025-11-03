"""EMERGENCY FIX: Database completo - ESEGUI QUESTO SU RENDER"""
import os
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not found!")
    exit(1)

# Fix postgres:// -> postgresql://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print(f"🔌 Connecting to database...")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("\n🔧 STEP 1: Add fingerprint columns to user_profiles...")
    
    try:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='user_profiles' AND column_name='fingerprint'
        """))
        
        if result.fetchone() is None:
            print("📝 Adding fingerprint column...")
            conn.execute(text("""
                ALTER TABLE user_profiles ADD COLUMN fingerprint VARCHAR(100)
            """))
            conn.execute(text("""
                CREATE UNIQUE INDEX IF NOT EXISTS ix_user_profiles_fingerprint 
                ON user_profiles(fingerprint)
            """))
            conn.commit()
            print("✅ fingerprint column added!")
        else:
            print("✓ fingerprint column already exists")
    except Exception as e:
        print(f"⚠️ fingerprint: {e}")
    
    try:
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='user_profiles' AND column_name='last_seen'
        """))
        
        if result.fetchone() is None:
            print("📝 Adding last_seen column...")
            conn.execute(text("""
                ALTER TABLE user_profiles ADD COLUMN last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """))
            conn.commit()
            print("✅ last_seen column added!")
        else:
            print("✓ last_seen column already exists")
    except Exception as e:
        print(f"⚠️ last_seen: {e}")
    
    print("\n🔧 STEP 2: Create community tables...")
    
    # Create all community tables
    tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS reflection_shares (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES user_profiles(id),
            text TEXT NOT NULL,
            visibility VARCHAR(20) DEFAULT 'anonymous',
            category VARCHAR(30),
            language VARCHAR(10) DEFAULT 'it',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_flagged BOOLEAN DEFAULT FALSE,
            flag_reason TEXT,
            sentiment_score FLOAT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reactions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES user_profiles(id),
            reflection_id INTEGER REFERENCES reflection_shares(id) ON DELETE CASCADE,
            reaction_type VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, reflection_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES user_profiles(id),
            reflection_id INTEGER REFERENCES reflection_shares(id) ON DELETE CASCADE,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_flagged BOOLEAN DEFAULT FALSE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS circles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            creator_id INTEGER REFERENCES user_profiles(id),
            invite_code VARCHAR(50) UNIQUE,
            max_members INTEGER DEFAULT 8,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS circle_members (
            id SERIAL PRIMARY KEY,
            circle_id INTEGER REFERENCES circles(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES user_profiles(id),
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            UNIQUE(circle_id, user_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS challenges (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            challenge_type VARCHAR(30),
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS challenge_participations (
            id SERIAL PRIMARY KEY,
            challenge_id INTEGER REFERENCES challenges(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES user_profiles(id),
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            days_completed INTEGER DEFAULT 0,
            last_checkin DATE,
            completed BOOLEAN DEFAULT FALSE,
            UNIQUE(challenge_id, user_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_bans (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES user_profiles(id),
            ban_type VARCHAR(20) NOT NULL,
            reason TEXT NOT NULL,
            violation_type VARCHAR(30),
            banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            active BOOLEAN DEFAULT TRUE,
            moderator_id INTEGER REFERENCES user_profiles(id),
            appeal_text TEXT,
            appeal_status VARCHAR(20),
            appeal_reviewed_at TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS moderation_logs (
            id SERIAL PRIMARY KEY,
            moderator_id INTEGER REFERENCES user_profiles(id),
            action_type VARCHAR(20) NOT NULL,
            target_type VARCHAR(20),
            target_id INTEGER,
            reason TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]
    
    for i, sql in enumerate(tables_sql, 1):
        try:
            conn.execute(text(sql))
            conn.commit()
            print(f"✅ Table {i}/9 created")
        except Exception as e:
            print(f"⚠️ Table {i}: {e}")
    
    print("\n✅ DATABASE FIX COMPLETE!")
    print("\n🎉 App should work now!")

print("\n✨ Done! Restart your Render service!")

