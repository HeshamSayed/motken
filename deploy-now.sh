#!/bin/bash

echo "🚀 Motken - Deploy Now"
echo "====================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Step 1: Merge deployment configuration${NC}"
echo "────────────────────────────────────────"
echo ""

# Check current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
    echo ""
    echo "You need to merge the deployment configuration to main branch."
    echo ""
    read -p "Do you want to merge to main now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Check if main branch exists
        if git show-ref --verify --quiet refs/heads/main; then
            TARGET_BRANCH="main"
        elif git show-ref --verify --quiet refs/heads/master; then
            TARGET_BRANCH="master"
        else
            echo -e "${RED}Neither main nor master branch found!${NC}"
            echo "Creating main branch..."
            git checkout -b main
            TARGET_BRANCH="main"
        fi

        if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
            echo "Merging $CURRENT_BRANCH to $TARGET_BRANCH..."
            git checkout $TARGET_BRANCH
            git merge $CURRENT_BRANCH --no-edit
        fi
    else
        echo "Skipping merge. Please merge manually before deploying."
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}Step 2: Push to GitHub${NC}"
echo "──────────────────────"
echo ""
echo "This will trigger automatic deployment via GitHub Actions."
echo ""
read -p "Push to GitHub now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin main 2>&1 || git push origin master 2>&1

    echo ""
    echo -e "${GREEN}✅ Code pushed to GitHub!${NC}"
    echo ""
    echo "GitHub Actions is now building and deploying your app."
    echo ""
    echo "Watch the deployment:"
    REPO_URL=$(git config --get remote.origin.url)
    if [[ $REPO_URL == *"github.com"* ]]; then
        # Extract owner/repo from URL
        REPO_PATH=$(echo $REPO_URL | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/.*github.com[:/]\(.*\)/\1/')
        echo "  → https://github.com/$REPO_PATH/actions"
    fi
else
    echo "Skipping push. Deploy when ready with: git push origin main"
    exit 0
fi

echo ""
echo -e "${BLUE}Step 3: Configure GitHub Secrets${NC}"
echo "─────────────────────────────────"
echo ""
echo "⚠️  IMPORTANT: Add these secrets to GitHub for automatic deployment:"
echo ""
echo "1. Go to your GitHub repository"
echo "2. Click Settings → Secrets and variables → Actions"
echo "3. Add these secrets:"
echo ""
echo "   ${YELLOW}NETLIFY_AUTH_TOKEN${NC}"
echo "   Get from: https://app.netlify.com/user/applications"
echo "   Click 'New access token' → Copy the token"
echo ""
echo "   ${YELLOW}NETLIFY_SITE_ID${NC}"
echo "   Value: timely-muffin-6841c8"
echo ""
echo "   ${YELLOW}API_BASE_URL${NC}"
echo "   Value: https://YOUR_BACKEND_URL.onrender.com/api/v1/"
echo "   (Get this after deploying backend to Render)"
echo ""
read -p "Press Enter when you've added the secrets..."

echo ""
echo -e "${BLUE}Step 4: Deploy Backend to Render${NC}"
echo "──────────────────────────────────"
echo ""
echo "1. Go to: https://render.com"
echo "2. Click 'New +' → 'Blueprint'"
echo "3. Connect your GitHub repository"
echo "4. Click 'Apply' (it will detect render.yaml)"
echo "5. Wait 5-10 minutes for deployment"
echo "6. Copy your backend URL (e.g., https://motken-backend-abc123.onrender.com)"
echo ""
echo "Add these environment variables in Render:"
echo "  - SECRET_KEY=<random-50-char-string>"
echo "  - DEBUG=False"
echo "  - ALLOWED_HOSTS=your-backend.onrender.com"
echo "  - CORS_ALLOWED_ORIGINS=https://timely-muffin-6841c8.netlify.app"
echo ""
read -p "Press Enter when backend is deployed..."

echo ""
echo -e "${BLUE}Step 5: Trigger Frontend Deployment${NC}"
echo "────────────────────────────────────"
echo ""
echo "If you already pushed to GitHub (Step 2), the frontend is deploying now!"
echo ""
echo "If not, or to redeploy:"
echo "  1. Go to GitHub → Actions tab"
echo "  2. Click 'Deploy Frontend to Netlify'"
echo "  3. Click 'Run workflow' → 'Run workflow'"
echo ""
echo "Or push any commit:"
echo "  git commit --allow-empty -m 'Trigger deployment'"
echo "  git push origin main"
echo ""

echo ""
echo -e "${GREEN}🎉 Deployment Setup Complete!${NC}"
echo ""
echo "Your app will be live at:"
echo "  Frontend: https://timely-muffin-6841c8.netlify.app"
echo "  Backend:  https://YOUR_BACKEND.onrender.com"
echo ""
echo "Monitor deployment:"
echo "  GitHub Actions: (check your repo → Actions tab)"
echo "  Netlify: https://app.netlify.com/sites/timely-muffin-6841c8/deploys"
echo "  Render: https://dashboard.render.com"
echo ""
echo "Takes approximately 10-15 minutes for first deployment."
echo ""
echo "For detailed instructions, see:"
echo "  - QUICK_START_AUTO_DEPLOY.md"
echo "  - AUTOMATIC_DEPLOYMENT_SETUP.md"
echo ""
