# Motken Mobile App

Flutter mobile application for Motken - Online Quran Learning Platform.

## Features

- **User Authentication**: JWT-based auth with biometric support
- **Teacher Discovery**: Browse and filter qualified Quran teachers
- **Session Booking**: Schedule and manage learning sessions
- **Video Calling**: Integrated Zoom SDK for live sessions
- **Payment Integration**: Paymob payment gateway
- **Progress Tracking**: Monitor learning progress and achievements
- **Multi-language**: Support for English and Arabic (RTL)
- **Offline Mode**: Access downloaded materials offline
- **Push Notifications**: Session reminders and updates

## Architecture

The app follows Clean Architecture principles with BLoC pattern:

```
lib/
├── core/               # Core functionality
│   ├── config/        # App configuration
│   ├── di/            # Dependency injection
│   ├── router/        # Navigation/routing
│   ├── theme/         # App theme
│   ├── utils/         # Utilities
│   └── widgets/       # Shared widgets
├── features/          # Feature modules
│   ├── auth/
│   ├── teachers/
│   ├── sessions/
│   ├── learning/
│   ├── payments/
│   └── profile/
└── main.dart
```

Each feature follows this structure:
```
feature/
├── data/
│   ├── datasources/
│   ├── models/
│   └── repositories/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
└── presentation/
    ├── bloc/
    ├── pages/
    └── widgets/
```

## Getting Started

### Prerequisites

- Flutter 3.16 or higher
- Dart 3.0 or higher
- iOS 12.0+ / Android 5.0+
- Xcode 14+ (for iOS)
- Android Studio / VS Code

### Installation

1. Clone the repository
```bash
cd mobile
```

2. Install dependencies
```bash
flutter pub get
```

3. Run code generation
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

4. Configure environment variables
Create a `.env` file in the mobile directory:
```env
API_BASE_URL=http://your-api-url.com/api/v1/
ZOOM_SDK_KEY=your_zoom_sdk_key
ZOOM_SDK_SECRET=your_zoom_sdk_secret
PAYMOB_API_KEY=your_paymob_api_key
PAYMOB_INTEGRATION_ID=your_integration_id
PAYMOB_IFRAME_ID=your_iframe_id
```

5. Run the app
```bash
flutter run
```

## Building for Production

### Android
```bash
flutter build apk --release
# or for app bundle
flutter build appbundle --release
```

### iOS
```bash
flutter build ios --release
```

## Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage

# Run integration tests
flutter drive --target=test_driver/app.dart
```

## Code Generation

The app uses code generation for models, routes, etc.:

```bash
# Generate once
flutter pub run build_runner build

# Watch for changes
flutter pub run build_runner watch

# Clean and rebuild
flutter pub run build_runner build --delete-conflicting-outputs
```

## Dependencies

See `pubspec.yaml` for full list of dependencies.

Key packages:
- **flutter_bloc**: State management
- **dio/retrofit**: HTTP client
- **go_router**: Navigation
- **hive**: Local storage
- **firebase**: Push notifications
- **zoom_sdk**: Video calling
- **local_auth**: Biometric authentication

## Performance Targets

- App size: < 50MB
- Cold start: < 3 seconds
- Frame rate: 60 FPS
- Crash-free rate: > 99.5%

## Contributing

1. Follow Flutter style guide
2. Write tests for new features
3. Update documentation
4. Create pull request

## License

Proprietary - All rights reserved
