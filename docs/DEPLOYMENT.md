# Deployment Guide - Nurse Eval AI

## Production Deployment

### Prerequisites
- Server with Docker & Docker Compose installed
- Domain name with DNS configured
- SSL certificates (Let's Encrypt recommended)
- PostgreSQL database (managed or self-hosted)

### Step 1: Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Create application user
sudo useradd -m -s /bin/bash nurseeval
sudo usermod -aG docker nurseeval
```

### Step 2: Application Setup

```bash
# Switch to application user
sudo su - nurseeval

# Clone repository
git clone https://github.com/lankamar/nurse-eval-ai.git
cd nurse-eval-ai

# Create production environment file
cp .env.example .env
```

### Step 3: Configure Environment

Edit `.env` with production values:

```env
# Database
POSTGRES_USER=nurseeval_prod
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=nurse_eval_prod

# Backend
SECRET_KEY=<generate-secure-32-char-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Sentry
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
ENVIRONMENT=production

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_SENTRY_DSN=https://your-frontend-sentry-dsn@sentry.io/project
```

### Step 4: SSL Configuration (Nginx)

Create `/etc/nginx/sites-available/nurseeval`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # API Docs
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Step 5: Deploy Application

```bash
# Build and start containers
docker-compose up -d --build

# Initialize database
docker-compose exec backend python -m app.db.seed

# Check logs
docker-compose logs -f
```

### Step 6: Monitoring Setup

1. **Sentry Configuration**
   - Create project in Sentry.io
   - Add DSN to environment variables
   - Verify error tracking

2. **Log Rotation**
```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/nurseeval

/var/log/nurseeval/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nurseeval nurseeval
    sharedscripts
}
```

### Step 7: Backup Configuration

```bash
# Database backup script
cat > ~/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/nurseeval/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
docker-compose exec -T db pg_dump -U nurseeval_prod nurse_eval_prod > $BACKUP_DIR/db_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql" -mtime +30 -delete
EOF

chmod +x ~/backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /home/nurseeval/backup.sh
```

### Step 8: Security Hardening

1. **Firewall Configuration**
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. **Database Security**
   - Use strong passwords
   - Restrict network access
   - Enable SSL connections

3. **Application Security**
   - Keep dependencies updated
   - Regular security audits
   - Monitor Sentry alerts

### Step 9: Health Monitoring

Create monitoring script:

```bash
cat > ~/health_check.sh << 'EOF'
#!/bin/bash
HEALTH_URL="http://localhost:8000/health"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $STATUS -ne 200 ]; then
    echo "Health check failed with status $STATUS"
    docker-compose restart backend
fi
EOF

chmod +x ~/health_check.sh

# Add to crontab (every 5 minutes)
crontab -e
# Add: */5 * * * * /home/nurseeval/health_check.sh
```

### Step 10: Updates and Maintenance

```bash
# Pull latest changes
cd ~/nurse-eval-ai
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Check status
docker-compose ps
docker-compose logs -f
```

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Use nginx or HAProxy
2. **Database**: PostgreSQL with read replicas
3. **Session Storage**: Redis for JWT blacklisting
4. **File Storage**: S3 or similar for PDFs

### Performance Optimization

1. **Database Indexing**: Already configured in models
2. **Caching**: Add Redis for frequent queries
3. **CDN**: For static frontend assets
4. **Connection Pooling**: Configure in production

## Troubleshooting

### Application won't start
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Verify environment variables
docker-compose config
```

### Database connection issues
```bash
# Check database status
docker-compose exec db psql -U nurseeval_prod -d nurse_eval_prod -c "SELECT 1;"

# Reset database (CAUTION: data loss)
docker-compose down -v
docker-compose up -d
docker-compose exec backend python -m app.db.seed
```

### Performance issues
```bash
# Monitor resource usage
docker stats

# Check database queries
docker-compose exec db psql -U nurseeval_prod -d nurse_eval_prod -c "SELECT * FROM pg_stat_activity;"
```

## Support

For issues or questions:
- Check GitHub Issues
- Review API documentation at `/docs`
- Contact system administrator
