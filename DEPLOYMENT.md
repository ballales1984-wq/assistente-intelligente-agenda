# 🚀 Deployment Production - Wallmind Agenda Intelligente

## 📋 Setup Iniziale

### 1. Clona Repository

```bash
git clone https://github.com/ballales1984-wq/assistente-intelligente-agenda.git
cd assistente-intelligente-agenda
```

### 2. Crea Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installa Dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura Environment Variables

```bash
# Copia template
cp .env.example .env

# Genera SECRET_KEY sicura
python -c "import secrets; print(secrets.token_hex(32))"

# Modifica .env con i tuoi valori
nano .env  # o usa qualsiasi editor
```

**Configurazione .env minima:**

```env
SECRET_KEY=your-generated-secret-key-here
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost:5432/agenda
ALLOWED_ORIGINS=https://tuodominio.com
LOG_LEVEL=INFO
```

### 5. Inizializza Database

```bash
python setup.py
```

### 6. Avvia Applicazione

#### Development
```bash
python run.py
```

#### Production (con Gunicorn)
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 "app:create_app()"
```

---

## ✅ Production Checklist

Prima di andare in produzione, verifica:

### **Security** 🔒
- [ ] SECRET_KEY generata e sicura (64+ caratteri hex)
- [ ] FLASK_ENV=production
- [ ] HTTPS configurato (certificato SSL)
- [ ] Firewall configurato (solo porte necessarie)
- [ ] Rate limiting attivo
- [ ] CORS configurato con domini specifici

### **Database** 💾
- [ ] PostgreSQL in produzione (non SQLite)
- [ ] Backup automatici configurati
- [ ] Connection pooling attivo
- [ ] Indici database ottimizzati

### **Monitoring** 📊
- [ ] Logs rotazione configurata (10MB max, 10 backup)
- [ ] Sentry/error tracking attivo (opzionale)
- [ ] Disk space monitoring
- [ ] Performance monitoring

### **Infrastructure** 🏗️
- [ ] Reverse proxy (Nginx/Apache)
- [ ] Process manager (systemd/supervisord)
- [ ] Auto-restart on crash
- [ ] Load balancer (se necessario)

### **Performance** ⚡
- [ ] Redis per rate limiting (invece di memory)
- [ ] Static files serviti da CDN/nginx
- [ ] Database query optimization
- [ ] Caching strategico

---

## 🐳 Deployment con Docker (Recommended)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crea logs directory
RUN mkdir -p logs

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:create_app()"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/agenda
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=agenda
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Deploy con Docker

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🌐 Deployment Cloud

### Heroku

```bash
# Login
heroku login

# Create app
heroku create wallmind-agenda

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Run migrations
heroku run python setup.py
```

### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. SSH into instance
ssh ubuntu@your-ec2-ip

# 3. Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv nginx

# 4. Clone repository
git clone https://github.com/your-repo/agenda.git
cd agenda

# 5. Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Configure environment
cp .env.example .env
nano .env  # Edit configuration

# 7. Setup systemd service
sudo nano /etc/systemd/system/agenda.service
```

**agenda.service:**

```ini
[Unit]
Description=Wallmind Agenda Intelligente
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/agenda
Environment="PATH=/home/ubuntu/agenda/venv/bin"
ExecStart=/home/ubuntu/agenda/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 "app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable agenda
sudo systemctl start agenda
sudo systemctl status agenda
```

---

## 🔧 Nginx Configuration

```nginx
server {
    listen 80;
    server_name tuodominio.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tuodominio.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static {
        alias /home/ubuntu/agenda/static;
        expires 30d;
    }

    # Proxy to Flask
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📊 Monitoring

### Log Analysis

```bash
# View logs
tail -f logs/app.log

# Parse JSON logs
cat logs/app.log | jq '.levelname, .message'

# Find errors
grep -i error logs/app.log | jq '.'

# Performance issues (slow requests)
cat logs/app.log | jq 'select(.duration_seconds > 1)'
```

### Health Check

```bash
# Simple health check endpoint
curl https://tuodominio.com/api/profilo
```

---

## 🔄 Update & Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart agenda

# Check status
sudo systemctl status agenda
```

### Database Backup

```bash
# PostgreSQL backup
pg_dump agenda > backup_$(date +%Y%m%d).sql

# Restore
psql agenda < backup_20250101.sql
```

### Log Rotation

Logs rotate automatically (10MB max, 10 backups).

Manual cleanup:

```bash
# Remove old logs
rm logs/app.log.*

# Archive
tar -czf logs_archive_$(date +%Y%m%d).tar.gz logs/
```

---

## 🐛 Troubleshooting

### App non parte

```bash
# Check logs
journalctl -u agenda -f

# Check Python errors
python run.py
```

### Database connection error

```bash
# Verify DATABASE_URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL
```

### Performance issues

```bash
# Check slow queries in logs
cat logs/app.log | jq 'select(.duration_seconds > 1)'

# Monitor server resources
htop
```

---

## 📞 Support

- **Documentation:** [README.md](README.md)
- **Issues:** https://github.com/ballales1984-wq/assistente-intelligente-agenda/issues
- **Email:** support@wallmind.com

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

<div align="center">

**🎊 Wallmind Agenda - Production Ready! 🎊**

v1.3.0 - 100% Production Ready

</div>

