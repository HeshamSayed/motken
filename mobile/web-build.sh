#!/bin/bash
# Flutter Web Build Script

echo "Building Motken Flutter Web App..."

# Enable web support
flutter config --enable-web

# Clean previous build
flutter clean

# Get dependencies
flutter pub get

# Build for web with optimizations
flutter build web --release \
  --web-renderer canvaskit \
  --base-href "/" \
  --dart-define=API_BASE_URL=https://your-backend-url.com

echo "Build complete! Output is in build/web/"
echo "Deploy the build/web directory to your hosting provider."
