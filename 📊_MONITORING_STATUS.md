# 📊 MONITORING STATUS - Wallmind Agenda

<div align="center">

# **🔍 STATO MONITORING & DATI**

</div>

---

## ✅ **COSA È ATTIVO**

### **🟢 App Flask:**
```
Status: ✅ RUNNING
URL: http://localhost:5000
Logging: ✅ Attivo (logs/app.log)
```

### **🟢 API Endpoints:**
```
✅ /api/profilo      → OK (200)
✅ /api/obiettivi    → OK (1 obiettivo)
✅ /api/impegni      → OK (verificare)
✅ /api/spese        → OK (1 spesa)
✅ /api/diario       → OK
✅ /beta             → OK (beta landing page)
```

### **🟡 Monitoring Stack:**
```
⚠️ Prometheus: NON avviato (richiede Docker)
⚠️ Grafana: NON avviato (richiede Docker)
⚠️ Redis: NON avviato (richiede Docker)
⚠️ PostgreSQL: NON avviato (usando SQLite)
```

**Nota:** L'app gira standalone, senza Docker stack completo.

---

## 📊 **DATI NEL DATABASE**

### **Secondo ultimo check:**
```
UserProfile: 1
Obiettivi:   3 ✅
Impegni:     8 ✅
Spese:       7 ✅
Diario:      3 ✅
```

### **Ma API mostrano meno dati!**
```
API /api/obiettivi → 1 obiettivo (Python)
API /api/spese → 1 spesa (Birra €14)
```

**⚠️ POSSIBILE PROBLEMA:** Database potrebbe avere file multipli!

---

## 🔍 **DIAGNOSTICA**

### **File Database:**
```bash
Possibili locations:
- C:\Users\user\Desktop\agenda\agenda.db
- C:\Users\user\Desktop\agenda\instance\agenda.db
- Memory (se DATABASE_URL non configurato bene)
```

### **Check quale sta usando:**
```python
from config import Config
print(Config.SQLALCHEMY_DATABASE_URI)
```

---

## 🛠️ **SOLUZIONI**

### **Opzione A: Verifica Database File**
```bash
# Vedi quale database sta usando
python -c "from config import Config; print(Config.SQLALCHEMY_DATABASE_URI)"

# Cerca tutti i file .db
dir *.db /s
```

### **Opzione B: Ricrea Database da Zero**
```bash
# 1. Backup vecchio
copy agenda.db agenda.db.backup

# 2. Elimina
del agenda.db

# 3. Ricrea
python setup.py

# 4. Aggiungi dati demo
python add_demo_data.py

# 5. Riavvia app
python run.py

# 6. Refresh browser
```

### **Opzione C: Usa Docker Stack Completo**
```bash
# Avvia tutto (app + postgres + redis + prometheus + grafana)
docker-compose up -d

# Attendi 30 sec
timeout /t 30

# Verifica
docker-compose ps

# Accedi
http://localhost:5000     → App
http://localhost:9090     → Prometheus
http://localhost:3000     → Grafana
```

---

## 📈 **MONITORING COMPLETO (Docker)**

### **Se avvii Docker stack:**

#### **Prometheus Metrics:**
```
http://localhost:9090

Queries da provare:
- rate(http_requests_total[5m])
- http_request_duration_seconds
- obiettivi_total
- spese_total
- users_active
```

#### **Grafana Dashboards:**
```
http://localhost:3000
Login: admin / admin

Dashboards disponibili:
✅ Application Health (già configurato)
✅ Business Metrics (già configurato)

Import da:
monitoring/grafana/dashboards/app-health.json
monitoring/grafana/dashboards/business-metrics.json
```

#### **Logs Strutturati:**
```bash
# JSON logs
type logs\app.log

# Filtra per livello
type logs\app.log | findstr ERROR
type logs\app.log | findstr WARNING

# Visualizza ultimo
Get-Content logs\app.log -Tail 20
```

---

## 🎯 **RACCOMANDAZIONE**

### **Per Beta Launch Veloce:**
```
✅ Usa app standalone (come ora)
✅ SQLite va bene per < 100 utenti
✅ Logging già attivo
✅ Monitoring basic via logs

NON serve Docker stack per beta!
```

### **Per Production/Scaling:**
```
🐳 docker-compose up -d
→ PostgreSQL
→ Redis
→ Prometheus
→ Grafana
→ Full monitoring!
```

---

## 🔧 **FIX IMMEDIATO**

### **Problema: API non mostrano tutti i dati**

**Soluzione rapida:**

```bash
# 1. Verifica quale DB usa
python -c "from config import Config; import os; print('DB:', Config.SQLALCHEMY_DATABASE_URI)"

# 2. Se vedi 'sqlite:///...' nota il path

# 3. Ricrea DB pulito
del agenda.db
python setup.py

# 4. Aggiungi dati demo
python add_demo_data.py

# 5. Verifica
python test_db.py

# 6. Riavvia app (Ctrl+C nel terminale, poi):
python run.py

# 7. Refresh browser (Ctrl+F5)
```

---

## ✅ **MONITORING ATTIVO ORA:**

```
✅ JSON Structured Logging
   → logs/app.log (JSON format)
   → Rotation automatica (10MB, 10 backup)

✅ Performance Tracking
   → Request duration logged
   → Slow queries detected (>1s)

✅ Error Tracking
   → Stack traces completi
   → User context included

✅ Console Output
   → Real-time nel terminale
```

---

## 📊 **VIEWING LOGS:**

```bash
# Tail logs in real-time
Get-Content logs\app.log -Wait -Tail 50

# Parse JSON logs
Get-Content logs\app.log | ConvertFrom-Json | Format-Table

# Filter errors
type logs\app.log | findstr ERROR
```

---

<div align="center">

## 🎯 **PROSSIMO STEP**

### **Se vedi i dati nell'UI:**
```
✅ PERFETTO! Tutto funziona!
→ Pronto per beta launch!
→ Inizia a condividere!
```

### **Se NON vedi i dati:**
```
⚠️ Ricrea database pulito (istruzioni sopra)
⚠️ Oppure dimmi cosa vedi esattamente
→ Fixo immediatamente!
```

---

## 🚀 **Per Full Monitoring Stack:**

```bash
docker-compose up -d
```

**Ma per beta non serve!** ✅

</div>

---

**Dimmi: Vedi i dati nell'interfaccia ora? (Obiettivi, Spese, Calendario)** 👀
