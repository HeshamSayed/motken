# Deployment Guide

## Production Deployment Checklist

### Backend (Django)

1. **Environment Configuration**
```bash
# Update .env file with production values
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379/1
```

2. **Database Setup**
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

3. **Security**
- Enable SSL/TLS
- Configure CORS properly
- Set up rate limiting
- Enable security headers
- Configure firewall rules

4. **Docker Deployment**
```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

### Mobile App (Flutter)

#### iOS Deployment

1. **Prepare for App Store**
```bash
# Update version in pubspec.yaml
version: 1.0.0+1

# Build release
flutter build ios --release

# Open in Xcode
open ios/Runner.xcworkspace
```

2. **App Store Connect**
- Configure app metadata
- Upload screenshots
- Set pricing
- Submit for review

#### Android Deployment

1. **Build Release**
```bash
# For APK
flutter build apk --release

# For App Bundle (recommended)
flutter build appbundle --release
```

2. **Google Play Console**
- Create app listing
- Upload app bundle
- Set content rating
- Submit for review

### Infrastructure

#### AWS Setup

1. **EC2 Instances**
- t3.medium or larger for backend
- Configure security groups
- Set up Elastic IP

2. **RDS PostgreSQL**
```bash
# Create RDS instance
# Configure security groups
# Enable automated backups
```

3. **ElastiCache Redis**
```bash
# Create Redis cluster
# Configure VPC
# Set up replication
```

4. **S3 Buckets**
```bash
# Create buckets for:
# - Static files
# - Media files
# - Backups
```

5. **CloudFront CDN**
- Configure distributions
- Set up SSL certificates
- Configure caching rules

#### Load Balancer

```bash
# Configure Application Load Balancer
# Set up health checks
# Configure auto-scaling
```

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        # Add deployment steps

  deploy-mobile:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build iOS/Android
        # Add build steps
```

## Monitoring

### Sentry Setup
```python
# Already configured in settings.py
SENTRY_DSN=your-sentry-dsn
```

### Logging
- Configure CloudWatch Logs
- Set up log aggregation
- Configure alerts

### Performance Monitoring
- Enable APM
- Set up uptime monitoring
- Configure performance alerts

## Backup Strategy

### Database Backups
```bash
# Daily automated backups
# Retention: 30 days
# Test restore procedures monthly
```

### Media Files Backup
```bash
# S3 versioning enabled
# Cross-region replication
```

## Scaling

### Horizontal Scaling
- Add more backend instances
- Configure load balancer
- Set up auto-scaling policies

### Database Scaling
- Enable read replicas
- Configure connection pooling
- Optimize queries

### Cache Scaling
- Use Redis cluster
- Configure eviction policies

## Security

### SSL/TLS
```bash
# Use Let's Encrypt for SSL certificates
certbot certonly --webroot -w /var/www/certbot -d yourdomain.com
```

### Firewall Rules
```bash
# Allow only necessary ports
# 80/443 for HTTP/HTTPS
# 22 for SSH (restrict to specific IPs)
```

### Regular Updates
```bash
# Keep dependencies updated
pip install --upgrade -r requirements.txt
flutter pub upgrade
```

## Post-Deployment

1. **Smoke Tests**
   - Test authentication
   - Test payment flow
   - Test video calling
   - Test booking system

2. **Performance Tests**
   - Load testing
   - Stress testing
   - API response times

3. **Monitoring Setup**
   - Configure alerts
   - Set up dashboards
   - Test notification channels

4. **Documentation**
   - Update API documentation
   - Update user guides
   - Document deployment process
