# Development Guide

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Flutter 3.16+
- Docker & Docker Compose
- Git

### Initial Setup

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/motken.git
cd motken
```

2. **Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env.example .env

# Edit .env with your local settings
```

3. **Database Setup**
```bash
# Create database
createdb motken_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

4. **Run Backend**
```bash
# Development server
python manage.py runserver

# Celery worker (in another terminal)
celery -A core worker -l info

# Celery beat (in another terminal)
celery -A core beat -l info
```

5. **Mobile Setup**
```bash
cd mobile

# Install dependencies
flutter pub get

# Run code generation
flutter pub run build_runner build

# Run app
flutter run
```

### Using Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Stop services
docker-compose down
```

## Project Structure

### Backend (Django)

```
backend/
├── core/              # Django settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── users/             # User management
├── teachers/          # Teacher profiles
├── sessions/          # Session booking
├── payments/          # Payment processing
├── learning/          # Learning content
├── api/               # API utilities
├── manage.py
└── requirements.txt
```

### Mobile (Flutter)

```
mobile/
├── lib/
│   ├── core/          # Core functionality
│   ├── features/      # Feature modules
│   └── main.dart
├── test/              # Unit tests
├── integration_test/  # Integration tests
└── pubspec.yaml
```

## Development Workflow

### Git Workflow

1. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make Changes**
```bash
git add .
git commit -m "Description of changes"
```

3. **Push to Remote**
```bash
git push origin feature/your-feature-name
```

4. **Create Pull Request**
- Open PR on GitHub
- Request review
- Address feedback
- Merge when approved

### Code Style

#### Python (Backend)
- Follow PEP 8
- Use Black for formatting
- Use isort for imports
- Max line length: 100

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8
```

#### Dart (Mobile)
- Follow Dart style guide
- Use dartfmt
- Max line length: 80

```bash
# Format code
dart format .

# Analyze
flutter analyze
```

### Testing

#### Backend Tests
```bash
# Run all tests
pytest

# With coverage
pytest --cov=.

# Specific app
pytest users/tests/

# Specific test
pytest users/tests/test_models.py::TestUserModel
```

#### Mobile Tests
```bash
# Unit tests
flutter test

# Integration tests
flutter drive --target=test_driver/app.dart

# Widget tests
flutter test test/widgets/
```

### Database Migrations

```bash
# Create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Rollback
python manage.py migrate users 0001
```

### Adding New Features

#### Backend (Django)

1. **Create Model**
```python
# app/models.py
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
```

2. **Create Serializer**
```python
# app/serializers.py
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

3. **Create View**
```python
# app/views.py
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

4. **Add URL**
```python
# app/urls.py
router.register(r'my-models', MyModelViewSet)
```

5. **Add Tests**
```python
# app/tests/test_models.py
def test_my_model_creation():
    obj = MyModel.objects.create(name="Test")
    assert obj.name == "Test"
```

#### Mobile (Flutter)

1. **Create Entity**
```dart
// domain/entities/my_entity.dart
class MyEntity {
  final String id;
  final String name;

  MyEntity({required this.id, required this.name});
}
```

2. **Create Model**
```dart
// data/models/my_model.dart
@JsonSerializable()
class MyModel extends MyEntity {
  factory MyModel.fromJson(Map<String, dynamic> json) =>
      _$MyModelFromJson(json);
}
```

3. **Create Repository**
```dart
// domain/repositories/my_repository.dart
abstract class MyRepository {
  Future<Either<Failure, List<MyEntity>>> getAll();
}
```

4. **Create Use Case**
```dart
// domain/usecases/get_my_entities.dart
class GetMyEntities {
  final MyRepository repository;

  Future<Either<Failure, List<MyEntity>>> call() =>
      repository.getAll();
}
```

5. **Create BLoC**
```dart
// presentation/bloc/my_bloc.dart
class MyBloc extends Bloc<MyEvent, MyState> {
  // Implementation
}
```

## API Development

### Adding New Endpoint

1. Define serializer
2. Create view/viewset
3. Add URL pattern
4. Write tests
5. Update API documentation

### Testing API

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Using httpie
http POST localhost:8000/api/v1/auth/login/ \
  email=test@example.com password=password
```

### API Documentation

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Schema: http://localhost:8000/api/schema/

## Debugging

### Backend

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use ipdb
import ipdb; ipdb.set_trace()

# Django shell
python manage.py shell

# Django shell with IPython
python manage.py shell_plus
```

### Mobile

```dart
// Print debug info
debugPrint('Debug message');

// Breakpoint in VS Code
// Add breakpoint in editor

// Flutter DevTools
flutter pub global activate devtools
flutter pub global run devtools
```

## Performance Optimization

### Backend

- Use select_related() and prefetch_related()
- Add database indexes
- Use caching (Redis)
- Optimize queries with django-debug-toolbar
- Use Celery for long-running tasks

### Mobile

- Use const constructors
- Implement lazy loading
- Optimize images
- Use cached_network_image
- Profile with Flutter DevTools

## Common Issues

### Backend

**Issue**: Database connection errors
```bash
# Solution: Check PostgreSQL is running
brew services start postgresql  # macOS
sudo systemctl start postgresql  # Linux
```

**Issue**: Migration conflicts
```bash
# Solution: Reset migrations (dev only!)
python manage.py migrate --fake app_name zero
python manage.py migrate app_name
```

### Mobile

**Issue**: Build fails after pub get
```bash
# Solution: Clean and rebuild
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

**Issue**: iOS build issues
```bash
# Solution: Clean pods
cd ios
rm -rf Pods Podfile.lock
pod install
cd ..
flutter clean
flutter build ios
```

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Flutter Documentation](https://docs.flutter.dev/)
- [BLoC Pattern](https://bloclibrary.dev/)
