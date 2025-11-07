# Getting Started with Motken

Welcome to Motken - Online Quran Learning Platform! This guide will help you get up and running quickly.

## 🚀 Quick Start

### Prerequisites

Make sure you have the following installed:
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Flutter 3.16+ (for mobile development)
- Docker & Docker Compose (recommended)

### Option 1: Using Docker (Recommended)

This is the fastest way to get started:

```bash
# 1. Clone the repository (if not already done)
cd motken

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env with your configuration
nano .env

# 4. Start all services
docker-compose up -d

# 5. Run database migrations
docker-compose exec backend python manage.py migrate

# 6. Create a superuser
docker-compose exec backend python manage.py createsuperuser

# 7. Access the application
# Backend API: http://localhost:8000
# Admin Panel: http://localhost:8000/admin
# API Documentation: http://localhost:8000/api/docs
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database
createdb motken_db

# 5. Copy and configure environment
cp ../.env.example ../.env
# Edit .env with your settings

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Run development server
python manage.py runserver
```

#### Start Celery Workers

In separate terminals:

```bash
# Terminal 1: Celery Worker
celery -A core worker -l info

# Terminal 2: Celery Beat (Scheduler)
celery -A core beat -l info
```

#### Mobile App Setup

```bash
# 1. Navigate to mobile directory
cd mobile

# 2. Install dependencies
flutter pub get

# 3. Run code generation (if needed)
flutter pub run build_runner build --delete-conflicting-outputs

# 4. Run the app
flutter run
```

## 📱 Testing the API

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "student",
    "phone_number": "+1234567890",
    "country": "USA"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "SecurePass123!"
  }'
```

Save the `access` token from the response for subsequent requests.

### 3. Get Current User

```bash
curl -X GET http://localhost:8000/api/v1/auth/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Browse Teachers

```bash
curl -X GET "http://localhost:8000/api/v1/teachers/profiles/?min_rating=4&max_price=50" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. View Packages

```bash
curl -X GET http://localhost:8000/api/v1/payments/packages/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔧 Configuration

### Environment Variables

Key environment variables to configure in `.env`:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=motken_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/1

# Paymob (Get from https://paymob.com)
PAYMOB_API_KEY=your-api-key
PAYMOB_INTEGRATION_ID=your-integration-id
PAYMOB_IFRAME_ID=your-iframe-id
PAYMOB_HMAC_SECRET=your-hmac-secret

# Zoom (Get from https://marketplace.zoom.us)
ZOOM_API_KEY=your-zoom-api-key
ZOOM_API_SECRET=your-zoom-api-secret
```

## 🎯 Next Steps

### 1. Create Sample Data

```bash
# Create a teacher
python manage.py shell
>>> from users.models import User
>>> from teachers.models import TeacherProfile
>>> teacher_user = User.objects.create_user(
...     email='teacher@example.com',
...     password='TeacherPass123!',
...     first_name='Ahmed',
...     last_name='Hassan',
...     user_type='teacher'
... )
>>> teacher_profile = TeacherProfile.objects.create(
...     user=teacher_user,
...     bio='Experienced Quran teacher with Ijazah',
...     years_of_experience=10,
...     specializations=['tajweed', 'memorization'],
...     education='Bachelor in Islamic Studies',
...     teaching_styles=['patient', 'structured'],
...     languages_spoken=['ar', 'en'],
...     session_30min_rate=15.00,
...     session_45min_rate=20.00,
...     session_60min_rate=25.00,
...     application_status='approved'
... )
```

### 2. Create Sample Packages

```bash
python manage.py shell
>>> from payments.models import Package
>>> Package.objects.create(
...     name='Basic Package',
...     package_type='basic',
...     description='Perfect for beginners',
...     session_count=4,
...     session_duration=30,
...     validity_days=30,
...     price=50.00,
...     currency='USD',
...     features=['4 Sessions', '30 minutes each', 'Session Recordings']
... )
```

### 3. Access Admin Panel

1. Go to http://localhost:8000/admin
2. Login with your superuser credentials
3. Explore and manage:
   - Users
   - Teachers
   - Sessions
   - Packages
   - Transactions
   - And more...

### 4. View API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **API Schema**: http://localhost:8000/api/schema/

## 📚 Key API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - Register
- `POST /api/v1/auth/login/` - Login
- `POST /api/v1/auth/token/refresh/` - Refresh token
- `GET /api/v1/auth/users/me/` - Get profile

### Teachers
- `GET /api/v1/teachers/profiles/` - List teachers
- `GET /api/v1/teachers/profiles/{id}/` - Teacher detail
- `POST /api/v1/teachers/profiles/apply/` - Apply as teacher

### Sessions
- `POST /api/v1/sessions/book/` - Book session
- `GET /api/v1/sessions/my_sessions/` - My sessions
- `POST /api/v1/sessions/{id}/cancel/` - Cancel session
- `GET /api/v1/sessions/{id}/join/` - Get Zoom link

### Payments
- `GET /api/v1/payments/packages/` - List packages
- `POST /api/v1/payments/transactions/initiate/` - Start payment
- `GET /api/v1/payments/subscriptions/my_subscription/` - My subscription

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Start PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS
```

### Redis Connection Error

```bash
# Check if Redis is running
redis-cli ping  # Should return PONG

# Start Redis
sudo systemctl start redis  # Linux
brew services start redis  # macOS
```

### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000  # Unix/macOS
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
python manage.py runserver 8001
```

### Docker Issues

```bash
# Stop all containers
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Rebuild containers
docker-compose build --no-cache

# View logs
docker-compose logs -f backend
```

## 💡 Tips

### 1. Development Workflow

```bash
# Make changes to models
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create test data
python manage.py shell

# Run tests
pytest

# Format code
black .
isort .
```

### 2. Monitoring Logs

```bash
# Backend logs (Django)
tail -f backend/logs/django.log

# Celery logs
celery -A core worker -l debug

# Docker logs
docker-compose logs -f
```

### 3. Database Management

```bash
# Backup database
pg_dump motken_db > backup.sql

# Restore database
psql motken_db < backup.sql

# Access database shell
python manage.py dbshell
```

## 🔒 Security Checklist

Before going to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set up monitoring (Sentry)
- [ ] Configure backup systems
- [ ] Review all environment variables
- [ ] Enable HTTPS only
- [ ] Configure CORS properly

## 📖 Further Reading

- [API Documentation](docs/API.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)

## 🆘 Getting Help

- Check the documentation in `docs/` folder
- Review `IMPLEMENTATION_SUMMARY.md` for feature details
- Check GitHub Issues
- Contact: support@motken.com

---

**Happy coding! 🎉**
