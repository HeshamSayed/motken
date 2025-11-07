# Motken - Online Quran Learning Platform

A production-ready mobile application connecting students with qualified Quran teachers for personalized online sessions at competitive prices (30-40% below market rates).

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.16+-blue.svg)](https://flutter.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Performance Targets](#performance-targets)
- [Contributing](#contributing)
- [License](#license)

## Overview

Motken is a comprehensive online Quran learning platform that connects students with qualified teachers for one-on-one sessions. The platform offers:

- 📱 Native mobile apps (iOS & Android)
- 👨‍🏫 Verified Quran teachers with Ijazah
- 📚 Multiple learning curricula (Reading, Tajweed, Memorization, Tafseer)
- 💰 Competitive pricing with flexible packages
- 🎥 Integrated video calling via Zoom SDK
- 📊 Progress tracking and achievements
- 💳 Secure payment processing via Paymob
- 🌍 Multi-language support (English/Arabic)

## Features

### User Management
- **Students**: Browse teachers, book sessions, track progress, manage payments
- **Teachers**: Manage profile, set availability, conduct sessions, receive payouts
- **Admin**: Complete control via Django Admin - users, content, pricing, analytics

### Core Functionality
- **Session Management**: Scheduling, booking, reminders, cancellations, recurring sessions
- **Learning System**: Multiple curricula, progress tracking, homework, lesson materials
- **Communication**: In-app chat, video calls with screen sharing, session recordings
- **Payments**: Multiple packages, auto-billing, multi-currency, teacher payouts
- **Quality Control**: Ratings, reviews, teacher verification, session monitoring

### Pricing Structure
- Trial sessions (free/discounted)
- Monthly packages: 4, 8, 12, 20 sessions
- Session durations: 30/45/60 minutes
- Competitive pricing (30-40% below market)

## Technology Stack

### Backend
- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL 15+ with proper indexing
- **Cache**: Redis 7+ for caching & Celery message broker
- **Authentication**: JWT with refresh tokens and biometric support
- **Video**: Zoom SDK integration
- **Payment**: Paymob payment gateway
- **Storage**: AWS S3 for media files
- **CDN**: CloudFlare

### Mobile
- **Framework**: Flutter 3.16+
- **State Management**: BLoC pattern
- **Storage**: Hive for local data, Flutter Secure Storage
- **Notifications**: Firebase Cloud Messaging
- **Authentication**: JWT + Biometric (Face ID, Touch ID, Fingerprint)
- **Offline**: Offline-first architecture

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry for error tracking
- **Server**: WSGI with Gunicorn
- **Proxy**: Nginx reverse proxy

## Project Structure

```
motken/
├── backend/                    # Django REST API
│   ├── core/                  # Django settings and configuration
│   ├── users/                 # User management (Students, Teachers, Admin)
│   ├── teachers/              # Teacher profiles and management
│   ├── sessions/              # Session booking and scheduling
│   ├── payments/              # Payment processing (Paymob)
│   ├── learning/              # Learning content and progress
│   ├── api/                   # API utilities and exceptions
│   ├── manage.py
│   └── requirements.txt
│
├── mobile/                     # Flutter mobile app
│   ├── lib/
│   │   ├── core/              # Core functionality
│   │   │   ├── config/        # App configuration
│   │   │   ├── theme/         # App theme
│   │   │   ├── router/        # Navigation
│   │   │   └── di/            # Dependency injection
│   │   ├── features/          # Feature modules
│   │   │   ├── auth/          # Authentication
│   │   │   ├── teachers/      # Teacher discovery
│   │   │   ├── sessions/      # Session booking
│   │   │   ├── learning/      # Learning content
│   │   │   ├── payments/      # Payments
│   │   │   └── profile/       # User profile
│   │   └── main.dart
│   ├── test/                  # Tests
│   └── pubspec.yaml
│
├── docker/                     # Docker configuration
│   ├── nginx/                 # Nginx configuration
│   └── ssl/                   # SSL certificates
│
├── docs/                       # Documentation
│   ├── API.md                 # API documentation
│   ├── DEVELOPMENT.md         # Development guide
│   └── DEPLOYMENT.md          # Deployment guide
│
├── .env.example               # Environment variables template
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image definition
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Python 3.11+
- Flutter 3.16+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)
- Git

### Quick Start with Docker

```bash
# Clone repository
git clone https://github.com/yourusername/motken.git
cd motken

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access the application
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin
# API Docs: http://localhost:8000/api/docs
```

### Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env.example ../.env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Mobile Setup

```bash
cd mobile

# Install dependencies
flutter pub get

# Run code generation
flutter pub run build_runner build

# Run on emulator/device
flutter run
```

#### Celery Setup (Required for background tasks)

```bash
# In separate terminals:

# Celery worker
celery -A core worker -l info

# Celery beat (scheduler)
celery -A core beat -l info
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[API Documentation](docs/API.md)**: Complete API reference with examples
- **[Development Guide](docs/DEVELOPMENT.md)**: Setup and development workflow
- **[Deployment Guide](docs/DEPLOYMENT.md)**: Production deployment instructions

### API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- Schema: http://localhost:8000/api/schema/

## Development

### Running Tests

#### Backend
```bash
cd backend
pytest                          # Run all tests
pytest --cov=.                  # With coverage
pytest users/tests/             # Specific app
```

#### Mobile
```bash
cd mobile
flutter test                    # Unit tests
flutter drive                   # Integration tests
```

### Code Style

#### Backend (Python)
```bash
black .                         # Format code
isort .                         # Sort imports
flake8                          # Lint
```

#### Mobile (Dart)
```bash
dart format .                   # Format code
flutter analyze                 # Analyze code
```

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Description"`
3. Push to remote: `git push origin feature/your-feature`
4. Create Pull Request for review

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed development guide.

## Deployment

### Production Deployment

1. **Configure Environment**
   - Update `.env` with production values
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`

2. **Build and Deploy**
```bash
# Backend
docker-compose -f docker-compose.prod.yml up -d

# Mobile
flutter build apk --release          # Android
flutter build ios --release          # iOS
```

3. **Post-Deployment**
   - Run migrations
   - Collect static files
   - Run smoke tests
   - Configure monitoring

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for complete deployment guide.

## Performance Targets

### Backend
- API response time < 200ms (95th percentile)
- Support 10,000+ concurrent users
- Handle 1000+ simultaneous video sessions
- 99.9% uptime

### Mobile
- App size < 50MB
- Cold start < 3 seconds
- Frame rate: 60 FPS
- Crash-free rate > 99.5%

### Business
- Page load time < 2 seconds
- Payment success rate > 95%
- App store rating > 4.5

## Development Phases

### Phase 1 (8 weeks) - MVP
- ✅ User authentication & profiles
- ✅ Teacher discovery & profiles
- ✅ Session booking system
- ✅ Payment integration (Paymob)
- ✅ Video calling (Zoom SDK)

### Phase 2 (6 weeks) - Learning Features
- 📚 Learning curriculum & lessons
- 📊 Progress tracking
- 📝 Homework system
- 💬 In-app messaging
- 📥 Learning materials

### Phase 3 (4 weeks) - Production Hardening
- 🔒 Security audit
- ⚡ Performance optimization
- 📈 Monitoring & logging
- 🧪 Load testing
- 📱 App store preparation

## Security Features

- SSL/TLS encryption
- JWT authentication with refresh tokens
- API rate limiting
- Request signing
- Certificate pinning
- GDPR compliance
- Parental controls for minors
- PCI compliance for payments
- Data encryption at rest and in transit

## Contributing

Please read [DEVELOPMENT.md](docs/DEVELOPMENT.md) for details on our code of conduct and development process.

## Support

For support and questions:
- 📧 Email: support@motken.com
- 📚 Documentation: [docs/](docs/)
- 🐛 Issues: GitHub Issues

## License

Proprietary - All rights reserved

---

**Built with ❤️ for Quran learners worldwide**
