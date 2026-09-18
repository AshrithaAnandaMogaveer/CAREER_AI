# Production Deployment Guide

## 🚀 Complete Deployment Checklist

### Pre-Deployment Requirements

#### 1. Environment Setup
- [ ] Production server (Linux recommended)
- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] PostgreSQL or MySQL database
- [ ] Domain name configured
- [ ] SSL certificate obtained

#### 2. Security Configuration
- [ ] Generate strong SECRET_KEY
- [ ] Configure production database credentials
- [ ] Set up firewall rules
- [ ] Enable HTTPS only
- [ ] Configure CORS for production domain
- [ ] Set secure cookie flags
- [ ] Enable rate limiting

#### 3. Performance Optimization
- [ ] Enable database connection pooling
- [ ] Set up Redis for caching
- [ ] Configure CDN for static assets
- [ ] Enable gzip compression
- [ ] Optimize database indexes
- [ ] Set up load balancer (if needed)

## 📦 Backend Deployment

### Step 1: Prepare Production Environment

```bash
# Create production directory
mkdir -p /var/www/community-app
cd /var/www/community-app

# Clone or copy your code
git clone <your-repo> .
# OR
scp -r career-guidance-ui/ user@server:/var/www/community-app/
```

### Step 2: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Install production server
pip install gunicorn psycopg2-binary
```

### Step 3: Configure Environment Variables

```bash
# Create .env file
cat > .env << EOF
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
DATABASE_URL=postgresql://user:password@localhost/community_db
FLASK_ENV=production
CORS_ORIGINS=https://yourdomain.com
EOF
```

### Step 4: Set Up Database

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE community_db;
CREATE USER community_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE community_db TO community_user;
\q

# Initialize database
python flask_cors_config.py
# Database tables will be created automatically
```

### Step 5: Configure Gunicorn

```bash
# Create gunicorn config
cat > gunicorn_config.py << EOF
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
EOF

# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown $USER:$USER /var/log/gunicorn
```

### Step 6: Create Systemd Service

```bash
# Create service file
sudo cat > /etc/systemd/system/community-app.service << EOF
[Unit]
Description=Community App Gunicorn Service
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/var/www/community-app
Environment="PATH=/var/www/community-app/venv/bin"
ExecStart=/var/www/community-app/venv/bin/gunicorn \\
    --config gunicorn_config.py \\
    flask_cors_config:app

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable community-app
sudo systemctl start community-app
sudo systemctl status community-app
```

## 🌐 Frontend Deployment

### Step 1: Build Production Bundle

```bash
cd career-guidance-ui

# Update API endpoint in code
# Change http://localhost:5000 to https://api.yourdomain.com

# Build
npm run build
```

### Step 2: Deploy to Web Server

#### Option A: Nginx (Recommended)

```bash
# Install Nginx
sudo apt install nginx

# Create Nginx config
sudo cat > /etc/nginx/sites-available/community-app << EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    root /var/www/community-app/build;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/community-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Option B: Apache

```bash
# Install Apache
sudo apt install apache2

# Enable required modules
sudo a2enmod proxy proxy_http rewrite ssl

# Create Apache config
sudo cat > /etc/apache2/sites-available/community-app.conf << EOF
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem

    DocumentRoot /var/www/community-app/build
    
    <Directory /var/www/community-app/build>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ProxyPass /api http://127.0.0.1:5000/api
    ProxyPassReverse /api http://127.0.0.1:5000/api
</VirtualHost>
EOF

# Enable site
sudo a2ensite community-app
sudo systemctl reload apache2
```

### Step 3: Set Up SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

## 🗄️ Database Optimization

### PostgreSQL Configuration

```sql
-- Create indexes (if not already created by models)
CREATE INDEX CONCURRENTLY idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX CONCURRENTLY idx_notifications_user_unread ON notifications(user_id, is_read);
CREATE INDEX CONCURRENTLY idx_messages_conversation ON messages(conversation_id, created_at);

-- Enable query logging for optimization
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

-- Analyze tables
ANALYZE;
```

### Database Backup

```bash
# Create backup script
cat > /usr/local/bin/backup-community-db.sh << EOF
#!/bin/bash
BACKUP_DIR="/var/backups/community-db"
DATE=\$(date +%Y%m%d_%H%M%S)
mkdir -p \$BACKUP_DIR

pg_dump community_db | gzip > \$BACKUP_DIR/backup_\$DATE.sql.gz

# Keep only last 7 days
find \$BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/backup-community-db.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-community-db.sh") | crontab -
```

## 📊 Monitoring & Logging

### Set Up Application Monitoring

```bash
# Install monitoring tools
pip install sentry-sdk

# Add to flask_cors_config.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Configure Logging

```python
# Add to flask_cors_config.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        '/var/log/community-app/app.log',
        maxBytes=10240000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Community app startup')
```

### System Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Set up log rotation
sudo cat > /etc/logrotate.d/community-app << EOF
/var/log/community-app/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 $USER $USER
    sharedscripts
}
EOF
```

## 🔒 Security Hardening

### Firewall Configuration

```bash
# Configure UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Fail2Ban Setup

```bash
# Install Fail2Ban
sudo apt install fail2ban

# Configure for Nginx
sudo cat > /etc/fail2ban/jail.local << EOF
[nginx-http-auth]
enabled = true

[nginx-noscript]
enabled = true

[nginx-badbots]
enabled = true

[nginx-noproxy]
enabled = true
EOF

sudo systemctl restart fail2ban
```

### Rate Limiting

```python
# Add to flask_cors_config.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Apply to specific routes
@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ... existing code
```

## 🚦 Performance Optimization

### Redis Caching

```bash
# Install Redis
sudo apt install redis-server

# Configure Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

```python
# Add to requirements.txt
redis==4.5.1
flask-caching==2.0.2

# Add to flask_cors_config.py
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

# Cache expensive queries
@app.route('/api/community/feed')
@cache.cached(timeout=300, query_string=True)
def get_feed():
    # ... existing code
```

### Database Connection Pooling

```python
# Update app_config.py
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

## 📈 Scaling Strategies

### Horizontal Scaling

```bash
# Set up load balancer (Nginx)
upstream backend {
    least_conn;
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    location /api {
        proxy_pass http://backend;
    }
}
```

### Database Replication

```sql
-- Set up read replicas for PostgreSQL
-- Master-slave replication configuration
-- Use pgpool-II for connection pooling and load balancing
```

## 🧪 Post-Deployment Testing

### Health Check Endpoints

```python
# Add to flask_cors_config.py
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/health')
def api_health():
    # Check database connection
    try:
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    })
```

### Smoke Tests

```bash
# Test backend
curl https://yourdomain.com/health
curl https://yourdomain.com/api/health

# Test authentication
curl -X POST https://yourdomain.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Test community endpoints
curl https://yourdomain.com/api/community/groups \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📋 Maintenance Tasks

### Daily Tasks
- [ ] Check application logs
- [ ] Monitor error rates
- [ ] Check disk space
- [ ] Verify backups completed

### Weekly Tasks
- [ ] Review performance metrics
- [ ] Check for security updates
- [ ] Analyze slow queries
- [ ] Review user feedback

### Monthly Tasks
- [ ] Update dependencies
- [ ] Security audit
- [ ] Performance optimization
- [ ] Capacity planning

## 🆘 Troubleshooting

### Common Issues

**Issue: 502 Bad Gateway**
```bash
# Check if backend is running
sudo systemctl status community-app

# Check logs
sudo journalctl -u community-app -n 50

# Restart service
sudo systemctl restart community-app
```

**Issue: Database Connection Errors**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Restart PostgreSQL
sudo systemctl restart postgresql
```

**Issue: High Memory Usage**
```bash
# Check memory
free -h

# Check processes
ps aux --sort=-%mem | head

# Restart services if needed
sudo systemctl restart community-app
```

## 📞 Support & Monitoring

### Set Up Alerts

```bash
# Install monitoring agent (example: Datadog, New Relic)
# Configure alerts for:
# - High error rates
# - Slow response times
# - High CPU/memory usage
# - Database connection issues
# - Disk space warnings
```

### Log Aggregation

```bash
# Set up centralized logging (ELK Stack, Splunk, etc.)
# Configure log shipping from application logs
```

## ✅ Final Checklist

- [ ] Backend deployed and running
- [ ] Frontend built and served
- [ ] SSL certificate installed
- [ ] Database configured and backed up
- [ ] Monitoring and logging set up
- [ ] Security hardening completed
- [ ] Performance optimization applied
- [ ] Health checks passing
- [ ] Documentation updated
- [ ] Team trained on deployment

---

**Deployment Status:** Ready for Production ✓

**Last Updated:** 2026-03-01
**Version:** 1.0.0
