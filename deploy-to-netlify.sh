#!/bin/bash

echo "🔧 Motken - Manual Netlify Deployment Helper"
echo "============================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -d "mobile" ]; then
    echo -e "${RED}Error: mobile directory not found!${NC}"
    echo "Please run this script from the motken root directory"
    exit 1
fi

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}Flutter is not installed!${NC}"
    echo ""
    echo "Please install Flutter first:"
    echo "https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo -e "${BLUE}Step 1: Get Backend URL${NC}"
echo "─────────────────────────"
echo ""
echo "First, deploy your backend to Render:"
echo "1. Go to: https://render.com"
echo "2. Create Blueprint from your GitHub repo"
echo "3. Wait for deployment to complete"
echo "4. Copy your backend URL (e.g., https://motken-backend-abc123.onrender.com)"
echo ""
read -p "Enter your backend URL (or press Enter to use localhost): " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    BACKEND_URL="http://localhost:8000"
    echo -e "${YELLOW}Using localhost backend${NC}"
else
    # Remove trailing slash if present
    BACKEND_URL=${BACKEND_URL%/}
    echo -e "${GREEN}Using: $BACKEND_URL${NC}"
fi

API_URL="${BACKEND_URL}/api/v1/"

echo ""
echo -e "${BLUE}Step 2: Building Flutter Web App${NC}"
echo "──────────────────────────────────"
echo "API URL: $API_URL"
echo ""

cd mobile

# Enable web support
echo "Enabling Flutter web..."
flutter config --enable-web

# Clean previous build
echo "Cleaning previous build..."
flutter clean

# Get dependencies
echo "Getting dependencies..."
flutter pub get

# Build for web
echo "Building for web (this may take 2-5 minutes)..."
flutter build web --release \
  --web-renderer canvaskit \
  --dart-define=API_BASE_URL=$API_URL

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Build completed successfully!${NC}"
    echo ""
    echo "Output directory: mobile/build/web"
    echo ""
    echo -e "${BLUE}Step 3: Deploy to Netlify${NC}"
    echo "─────────────────────────"
    echo ""
    echo "Now deploy to your Netlify site:"
    echo ""
    echo "Option A - Drag & Drop (Easiest):"
    echo "  1. Go to: https://app.netlify.com/drop"
    echo "  2. Drag the 'build/web' folder and drop it"
    echo "  3. Your site will be live instantly!"
    echo ""
    echo "Option B - Connect to Existing Site:"
    echo "  1. Go to: https://app.netlify.com/sites/timely-muffin-6841c8/deploys"
    echo "  2. Scroll down to 'Need to deploy manually?'"
    echo "  3. Drag the 'build/web' folder"
    echo ""
    echo "Option C - Netlify CLI:"
    echo "  1. npm install -g netlify-cli"
    echo "  2. netlify login"
    echo "  3. netlify deploy --prod --dir=build/web --site=timely-muffin-6841c8"
    echo ""
    echo -e "${BLUE}Step 4: Update Backend CORS${NC}"
    echo "───────────────────────────"
    echo ""
    echo "After deploying, update your backend CORS settings:"
    echo "  1. Go to Render → Your backend service"
    echo "  2. Environment → Add/Update variable:"
    echo "     CORS_ALLOWED_ORIGINS=https://timely-muffin-6841c8.netlify.app"
    echo "  3. Save and redeploy backend"
    echo ""
    echo -e "${GREEN}🎉 Your app is ready to deploy!${NC}"
    echo ""
    
    # Open build folder
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open build/web
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open build/web 2>/dev/null || echo "Build folder: $(pwd)/build/web"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        explorer build/web
    fi
else
    echo ""
    echo -e "${RED}❌ Build failed!${NC}"
    echo ""
    echo "Check the error messages above."
    echo "Common issues:"
    echo "  - Missing dependencies: Run 'flutter pub get'"
    echo "  - Flutter not configured: Run 'flutter doctor'"
    exit 1
fi
