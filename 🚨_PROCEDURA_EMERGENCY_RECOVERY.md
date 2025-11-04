# 🚨 PROCEDURA EMERGENCY RECOVERY

**In caso di crash o problemi critici - SEGUI QUESTO!**

---

## ⚡ RECOVERY VELOCE (2 minuti)

Se la chat smette di funzionare:

```bash
git reset --hard fce74df
git push origin main --force
```

**Aspetta 5 minuti → Chat torna online!**

---

## 🔒 COMMIT SICURI

Usa questi in ordine se fce74df non funziona:

**1. fce74df** - "Fix: Riattiva campi condivisione" (PRINCIPALE)
- Ha fingerprinting
- Database allineato
- Tutto funziona

**2. cf255c0** - "Final Report: App testata 100%"
- App testata completa
- Senza fingerprinting
- Fallback sicuro

**3. 35ecc6b** - "Feature: Condivisione messaggi"
- Condivisione base
- Stabile
- Ultimo resort

---

## 🛠️ SE ANCORA NON FUNZIONA

### **Problema: Database disallineato**

**Soluzione:**

1. Vai su Render dashboard
2. Clicca database "agenda_db_bs07"
3. Tab "Shell"
4. Esegui:

```sql
-- Verifica colonne
\d user_profiles;

-- Se mancano colonne fingerprint:
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS token VARCHAR(64);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS fingerprint VARCHAR(100);
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS ip_hash VARCHAR(64);
```

5. Riavvia web service
6. Testa chat

---

## 📞 SUPPORTO

**Se proprio non funziona:**

1. Leggi file: `✅_APP_FUNZIONANTE_5NOV_2025.md`
2. Controlla BACKUP: `BACKUP_LAVORO_4NOV_2025/`
3. Aspetta domani con calma

---

**NON FARE MAI:**
- ❌ Reset multipli consecutivi
- ❌ Modifiche senza test
- ❌ Push durante Product Hunt

**FAI SEMPRE:**
- ✅ Un commit alla volta
- ✅ Aspetta deploy completo
- ✅ Testa prima di continuare

---

**🔒 KEEP CALM AND USE fce74df!**

