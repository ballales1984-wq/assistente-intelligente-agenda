-- FIX URGENTE DATABASE RENDER
-- Questo script rimuove e ricrea le colonne Telegram nel database

-- Step 1: Drop existing indexes
DROP INDEX IF EXISTS ix_user_profiles_telegram_id;

-- Step 2: Drop columns
ALTER TABLE user_profiles DROP COLUMN IF EXISTS telegram_id CASCADE;
ALTER TABLE user_profiles DROP COLUMN IF EXISTS telegram_username CASCADE;

-- Step 3: Re-add columns as nullable (per compatibilità)
ALTER TABLE user_profiles ADD COLUMN telegram_id VARCHAR(50);
ALTER TABLE user_profiles ADD COLUMN telegram_username VARCHAR(100);

-- Step 4: Re-create index (non unique per evitare conflitti)
CREATE INDEX IF NOT EXISTS ix_user_profiles_telegram_id ON user_profiles(telegram_id);

-- Step 5: Verify
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'user_profiles' 
AND column_name IN ('telegram_id', 'telegram_username');

