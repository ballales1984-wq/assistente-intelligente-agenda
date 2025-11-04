"""REBUILD COMPLETO - Crea tutte le tabelle da zero se necessario"""
from app import create_app, db
from sqlalchemy import text, inspect

print("🔧 REBUILD COMPLETO DATABASE...")

app = create_app()

with app.app_context():
    # Get current tables
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()
    
    print(f"\n📊 Tabelle esistenti: {len(existing_tables)}")
    for table in sorted(existing_tables):
        print(f"  - {table}")
    
    # Import ALL models to ensure they're registered
    print("\n📦 Importing models...")
    try:
        from app.models import UserProfile, Obiettivo, Impegno, DiarioGiornaliero, Spesa
        print("✅ Base models imported")
    except Exception as e:
        print(f"⚠️ Base models: {e}")
    
    try:
        from app.models.community import (
            ReflectionShare, Reaction, Comment, Circle, CircleMember,
            Challenge, ChallengeParticipation, UserBan, ModerationLog
        )
        print("✅ Community models imported")
    except Exception as e:
        print(f"⚠️ Community models: {e}")
    
    # Create ALL tables (safe - doesn't drop existing)
    print("\n🔨 Creating all tables...")
    db.create_all()
    print("✅ db.create_all() completed")
    
    # Now add missing columns to existing tables
    print("\n🔧 Adding missing columns to user_profiles...")
    
    with db.engine.connect() as conn:
        # Check and add fingerprint
        try:
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='user_profiles' AND column_name='fingerprint'
            """))
            
            if not result.fetchone():
                print("📝 Adding fingerprint column...")
                conn.execute(text("ALTER TABLE user_profiles ADD COLUMN fingerprint VARCHAR(100)"))
                conn.commit()
                print("✅ fingerprint added")
            else:
                print("✓ fingerprint exists")
        except Exception as e:
            print(f"  fingerprint: {e}")
        
        # Check and add last_seen
        try:
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='user_profiles' AND column_name='last_seen'
            """))
            
            if not result.fetchone():
                print("📝 Adding last_seen column...")
                conn.execute(text("ALTER TABLE user_profiles ADD COLUMN last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
                conn.commit()
                print("✅ last_seen added")
            else:
                print("✓ last_seen exists")
        except Exception as e:
            print(f"  last_seen: {e}")
    
    # Add sharing columns to diario table
    print("\n🔧 Adding sharing columns to diario...")
    
    with db.engine.connect() as conn:
        # Check and add share_token
        try:
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='diario' AND column_name='share_token'
            """))
            
            if not result.fetchone():
                print("📝 Adding share_token column...")
                conn.execute(text("ALTER TABLE diario ADD COLUMN share_token VARCHAR(64)"))
                conn.commit()
                print("✅ share_token added")
            else:
                print("✓ share_token exists")
        except Exception as e:
            print(f"  share_token: {e}")
        
        # Check and add is_public
        try:
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='diario' AND column_name='is_public'
            """))
            
            if not result.fetchone():
                print("📝 Adding is_public column...")
                conn.execute(text("ALTER TABLE diario ADD COLUMN is_public BOOLEAN DEFAULT FALSE"))
                conn.commit()
                print("✅ is_public added")
            else:
                print("✓ is_public exists")
        except Exception as e:
            print(f"  is_public: {e}")
        
        # Check and add share_count
        try:
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='diario' AND column_name='share_count'
            """))
            
            if not result.fetchone():
                print("📝 Adding share_count column...")
                conn.execute(text("ALTER TABLE diario ADD COLUMN share_count INTEGER DEFAULT 0"))
                conn.commit()
                print("✅ share_count added")
            else:
                print("✓ share_count exists")
        except Exception as e:
            print(f"  share_count: {e}")
        
        # Create unique index on share_token
        try:
            conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_diario_share_token ON diario (share_token)"))
            conn.commit()
            print("✅ Unique index on share_token created")
        except Exception as e:
            print(f"  index: {e}")
    
    # Verify all tables now exist
    inspector = inspect(db.engine)
    final_tables = inspector.get_table_names()
    
    print(f"\n✅ Final table count: {len(final_tables)}")
    
    expected_tables = [
        'user_profiles', 'obiettivi', 'impegni', 'diario', 'spese',
        'reflection_shares', 'reactions', 'comments', 'circles', 'circle_members',
        'challenges', 'challenge_participations', 'user_bans', 'moderation_logs',
        'beta_signups'
    ]
    
    print("\n🔍 Verification:")
    missing = []
    for table in expected_tables:
        if table in final_tables:
            print(f"  ✅ {table}")
        else:
            print(f"  ❌ {table} MISSING!")
            missing.append(table)
    
    if missing:
        print(f"\n⚠️ {len(missing)} tables still missing!")
    else:
        print("\n🎉 ALL TABLES PRESENT!")
    
    print("\n✨ Database rebuild complete!")

