"""Migration: Add fingerprint and last_seen columns to user_profiles"""
from app import create_app, db
from sqlalchemy import text

print("🔧 Migration: Adding fingerprint columns to user_profiles...")

app = create_app()

with app.app_context():
    try:
        # Check if columns exist
        result = db.session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='user_profiles' 
            AND column_name IN ('fingerprint', 'last_seen')
        """))
        existing_columns = [row[0] for row in result]
        
        print(f"✓ Existing columns: {existing_columns}")
        
        # Add fingerprint column if doesn't exist
        if 'fingerprint' not in existing_columns:
            print("📝 Adding 'fingerprint' column...")
            db.session.execute(text("""
                ALTER TABLE user_profiles 
                ADD COLUMN fingerprint VARCHAR(100) UNIQUE
            """))
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_user_profiles_fingerprint 
                ON user_profiles(fingerprint)
            """))
            print("✅ 'fingerprint' column added!")
        else:
            print("✓ 'fingerprint' column already exists")
        
        # Add last_seen column if doesn't exist
        if 'last_seen' not in existing_columns:
            print("📝 Adding 'last_seen' column...")
            db.session.execute(text("""
                ALTER TABLE user_profiles 
                ADD COLUMN last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """))
            print("✅ 'last_seen' column added!")
        else:
            print("✓ 'last_seen' column already exists")
        
        db.session.commit()
        print("\n🎉 Migration completed successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise

print("\n✨ Done!")

