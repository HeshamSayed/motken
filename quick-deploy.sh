#!/bin/bash

echo "🚀 Motken Quick Deployment Script"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}Error: Please run this script from the motken root directory${NC}"
    exit 1
fi

echo "Choose deployment option:"
echo "1) Local Docker Deployment (for testing)"
echo "2) Prepare for Render Deployment (cloud)"
echo "3) Prepare for Railway Deployment (cloud)"
echo "4) Build Flutter Web App"
echo ""
read -p "Enter option (1-4): " option

case $option in
    1)
        echo -e "${BLUE}Starting local Docker deployment...${NC}"
        
        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
            exit 1
        fi
        
        # Start services
        echo "Starting services..."
        docker-compose up -d
        
        # Wait for services to be ready
        echo "Waiting for services to start..."
        sleep 10
        
        # Run migrations
        echo "Running database migrations..."
        docker-compose exec backend python manage.py migrate
        
        # Create superuser prompt
        echo -e "${GREEN}Services started successfully!${NC}"
        echo ""
        echo "Create a superuser account:"
        docker-compose exec backend python manage.py createsuperuser
        
        echo ""
        echo -e "${GREEN}✅ Deployment complete!${NC}"
        echo ""
        echo "Access your application:"
        echo "  - Backend API: http://localhost:8000/api/v1/"
        echo "  - Admin Panel: http://localhost:8000/admin/"
        echo "  - API Docs: http://localhost:8000/api/schema/swagger-ui/"
        echo ""
        echo "View logs: docker-compose logs -f"
        echo "Stop services: docker-compose down"
        ;;
        
    2)
        echo -e "${BLUE}Preparing for Render deployment...${NC}"
        
        # Check if render.yaml exists
        if [ ! -f "render.yaml" ]; then
            echo -e "${RED}render.yaml not found!${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${GREEN}✅ Render configuration is ready!${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Push your code to GitHub:"
        echo "   git add ."
        echo "   git commit -m 'Add deployment configuration'"
        echo "   git push origin main"
        echo ""
        echo "2. Go to https://render.com and sign up"
        echo "3. Click 'New +' → 'Blueprint'"
        echo "4. Connect your GitHub repository"
        echo "5. Render will detect render.yaml and deploy automatically"
        echo ""
        echo "6. Set these environment variables in Render:"
        echo "   - SECRET_KEY (generate a random 50+ char string)"
        echo "   - ALLOWED_HOSTS (your-backend.onrender.com)"
        echo "   - CORS_ALLOWED_ORIGINS (https://your-frontend-url.com)"
        echo "   - STRIPE_SECRET_KEY (optional)"
        echo "   - STRIPE_PUBLISHABLE_KEY (optional)"
        echo ""
        echo "See DEPLOYMENT.md for complete instructions"
        ;;
        
    3)
        echo -e "${BLUE}Preparing for Railway deployment...${NC}"
        
        # Check if railway.json exists
        if [ ! -f "backend/railway.json" ]; then
            echo -e "${RED}backend/railway.json not found!${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${GREEN}✅ Railway configuration is ready!${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Install Railway CLI:"
        echo "   npm install -g @railway/cli"
        echo ""
        echo "2. Login to Railway:"
        echo "   railway login"
        echo ""
        echo "3. Deploy backend:"
        echo "   cd backend"
        echo "   railway init"
        echo "   railway up"
        echo ""
        echo "4. Add database:"
        echo "   railway add --database postgresql"
        echo "   railway add --database redis"
        echo ""
        echo "See DEPLOYMENT.md for complete instructions"
        ;;
        
    4)
        echo -e "${BLUE}Building Flutter web app...${NC}"
        
        # Check if Flutter is installed
        if ! command -v flutter &> /dev/null; then
            echo -e "${RED}Flutter is not installed.${NC}"
            echo "Install Flutter from: https://flutter.dev/docs/get-started/install"
            exit 1
        fi
        
        cd mobile
        
        # Enable web
        flutter config --enable-web
        
        # Clean
        echo "Cleaning previous build..."
        flutter clean
        
        # Get dependencies
        echo "Getting dependencies..."
        flutter pub get
        
        # Build
        echo "Building for web..."
        read -p "Enter your backend API URL (e.g., https://your-backend.onrender.com/api/v1/): " api_url
        
        flutter build web --release \
          --web-renderer canvaskit \
          --dart-define=API_BASE_URL=$api_url
        
        echo ""
        echo -e "${GREEN}✅ Build complete!${NC}"
        echo ""
        echo "Output directory: mobile/build/web"
        echo ""
        echo "Deploy options:"
        echo "1. Netlify: Drag and drop 'build/web' folder to netlify.com"
        echo "2. Vercel: Run 'vercel' in mobile directory"
        echo "3. Firebase: Run 'firebase deploy' in mobile directory"
        echo ""
        echo "See DEPLOYMENT.md for complete instructions"
        ;;
        
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac
