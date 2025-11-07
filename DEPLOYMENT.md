# Motken Deployment Guide

Complete guide to deploy the Motken Quran Learning Platform online for browser testing.

## Table of Contents
- [Quick Start Options](#quick-start-options)
- [Backend Deployment](#backend-deployment)
- [Frontend Deployment](#frontend-deployment)
- [Environment Configuration](#environment-configuration)
- [Testing](#testing)

---

## Quick Start Options

### Option 1: Deploy to Render (Recommended - Free Tier Available)
**Backend + Database + Redis** - All in one

1. Create account at [render.com](https://render.com)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml` and deploy everything
5. Set environment variables in Render dashboard
6. Wait 5-10 minutes for deployment

**Frontend on Netlify**
1. Create account at [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub repository
4. Set base directory to `mobile`
5. Netlify will auto-detect `netlify.toml` and build
6. Your app will be live at `https://your-app.netlify.app`

### Option 2: Deploy to Railway (Easy, Paid)
**Backend Deployment**

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will detect `railway.json`
5. Add PostgreSQL and Redis from Railway marketplace
6. Set environment variables
7. Deploy!

### Option 3: Docker + Any Host
Use Docker Compose for local testing or deploy to any VPS:

```bash
# Clone repository
git clone <your-repo>
cd motken

# Start all services
docker-compose up -d

# Access at:
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin
```

---

## Backend Deployment (Detailed)

### 1. Render Deployment

**Step 1: Push code to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

**Step 2: Deploy on Render**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Blueprint"
3. Connect your GitHub account
4. Select the `motken` repository
5. Render will read `render.yaml` and create:
   - Web Service (Django backend)
   - PostgreSQL Database
   - Redis Instance
   - 2 Worker Services (Celery + Beat)

**Step 3: Configure Environment Variables**
In Render dashboard, set these environment variables for the backend service:

```bash
# Required
DEBUG=False
SECRET_KEY=<generate-random-secret-key>
ALLOWED_HOSTS=your-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.netlify.app

# Payment (Stripe)
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key

# Video (Zoom - Optional)
ZOOM_API_KEY=your_zoom_key
ZOOM_API_SECRET=your_zoom_secret
```

**Step 4: Database Migration**
After deployment, run migrations:
1. Go to Shell in Render dashboard
2. Run: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`

**Step 5: Test Backend**
Visit: `https://your-backend.onrender.com/api/v1/health/`

### 2. Railway Deployment

**Step 1: Install Railway CLI (Optional)**
```bash
npm install -g @railway/cli
railway login
```

**Step 2: Deploy**
```bash
cd motken/backend
railway init
railway up
```

**Step 3: Add Database**
```bash
railway add --database postgresql
railway add --database redis
```

**Step 4: Set Environment Variables**
```bash
railway variables set DEBUG=False
railway variables set SECRET_KEY=<your-secret-key>
railway variables set ALLOWED_HOSTS=your-app.railway.app
```

### 3. Docker Deployment (Any VPS)

**Prerequisites:**
- VPS with Docker and Docker Compose
- Domain name (optional)

**Deployment Steps:**
```bash
# SSH into your VPS
ssh user@your-vps-ip

# Clone repository
git clone <your-repo>
cd motken

# Copy and configure environment
cp backend/.env.production.example backend/.env
nano backend/.env  # Edit with your settings

# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Your API is live at: http://your-vps-ip:8000
```

---

## Frontend Deployment (Flutter Web)

### Option 1: Netlify (Recommended)

**Step 1: Build Flutter Web Locally (Optional)**
```bash
cd mobile
chmod +x web-build.sh
./web-build.sh
```

**Step 2: Deploy to Netlify**

**Method A: Connect GitHub (Automatic)**
1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub and select repository
4. Configure:
   - Base directory: `mobile`
   - Build command: `flutter build web --release`
   - Publish directory: `mobile/build/web`
5. Click "Deploy"

**Method B: Manual Upload**
1. Build locally: `cd mobile && flutter build web --release`
2. Go to Netlify → "Sites" → "Add new site" → "Deploy manually"
3. Drag and drop the `mobile/build/web` folder
4. Done!

**Step 3: Configure Environment Variables**
In Netlify dashboard:
1. Go to Site settings → Environment variables
2. Add: `API_BASE_URL=https://your-backend.onrender.com/api/v1/`

**Step 4: Set up Redirects (Already configured in netlify.toml)**
Netlify will automatically handle SPA routing.

### Option 2: Vercel

**Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

**Step 2: Deploy**
```bash
cd mobile
vercel
```

Follow the prompts and your app will be live!

### Option 3: Firebase Hosting

**Step 1: Install Firebase CLI**
```bash
npm install -g firebase-tools
firebase login
```

**Step 2: Initialize Firebase**
```bash
cd mobile
firebase init hosting
```

Select options:
- Public directory: `build/web`
- Single-page app: Yes
- Set up automatic builds: No

**Step 3: Build and Deploy**
```bash
flutter build web --release
firebase deploy
```

Your app will be live at: `https://your-project.firebaseapp.com`

---

## Environment Configuration

### Backend Environment Variables

Create `backend/.env` with these variables:

```bash
# Django Core
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-min-50-chars
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# Stripe Payment
STRIPE_SECRET_KEY=sk_live_your_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret

# Zoom SDK (Optional)
ZOOM_API_KEY=your_zoom_key
ZOOM_API_SECRET=your_zoom_secret

# AWS S3 (Optional - for media storage)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

### Frontend Environment Variables

Set these during build:

```bash
# Build with custom API URL
flutter build web --release \
  --dart-define=API_BASE_URL=https://your-backend.onrender.com/api/v1/
```

Or set in hosting platform (Netlify/Vercel):
```bash
API_BASE_URL=https://your-backend.onrender.com/api/v1/
```

---

## Testing Your Deployment

### 1. Test Backend API

**Health Check:**
```bash
curl https://your-backend.onrender.com/api/v1/health/
```

**API Documentation:**
Visit: `https://your-backend.onrender.com/api/schema/swagger-ui/`

**Admin Panel:**
Visit: `https://your-backend.onrender.com/admin/`

### 2. Test Frontend

Visit your deployed app: `https://your-app.netlify.app`

**Test these flows:**
1. **Registration**: Click "Register" → Fill form → Create account
2. **Login**: Use credentials → Should redirect to home
3. **Browse Teachers**: Navigate to teachers list → See real data from backend
4. **Book Session**: Click teacher → View details → Book session
5. **Payments**: Go to packages → Select package → Initiate payment

### 3. Check Integration

**Test API Connection:**
1. Open browser console (F12)
2. Go to Network tab
3. Try logging in
4. Check if API requests go to your backend URL
5. Should see 200 responses

**Common Issues:**
- **CORS Error**: Add frontend URL to `CORS_ALLOWED_ORIGINS` in backend
- **API Not Found**: Check `API_BASE_URL` in frontend build
- **500 Errors**: Check backend logs in Render/Railway dashboard

---

## Quick Deploy Commands

### Complete Deployment (All Platforms)

**Backend to Render:**
```bash
# Push code
git push origin main

# Render will auto-deploy from render.yaml
# Just connect GitHub repo to Render
```

**Frontend to Netlify:**
```bash
# Option 1: GitHub (Automatic)
# Just connect repo to Netlify

# Option 2: Manual
cd mobile
flutter build web --release --dart-define=API_BASE_URL=https://your-backend.onrender.com/api/v1/
netlify deploy --prod --dir=build/web
```

### Local Testing with Docker

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop everything
docker-compose down

# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin
# API Docs: http://localhost:8000/api/schema/swagger-ui/
```

---

## Recommended Setup for Browser Testing

**Backend**: Render (Free tier) - https://your-app.onrender.com
**Frontend**: Netlify (Free tier) - https://your-app.netlify.app
**Database**: Render PostgreSQL (Free tier)
**Redis**: Render Redis (Free tier)

**Total Cost**: $0 (Free tier for all services)

**Setup Time**: ~15 minutes

**Steps:**
1. Push code to GitHub
2. Connect Render for backend (uses render.yaml)
3. Connect Netlify for frontend (uses netlify.toml)
4. Set environment variables
5. Test!

---

## Support and Troubleshooting

### Common Errors

**1. CORS Error in Browser**
```
Access to XMLHttpRequest blocked by CORS policy
```
**Fix**: Add your frontend URL to `CORS_ALLOWED_ORIGINS` in backend `.env`

**2. API Connection Failed**
```
Network Error / Connection Refused
```
**Fix**: 
- Check backend is running
- Verify `API_BASE_URL` in frontend build
- Check backend logs for errors

**3. Database Migration Failed**
```
No such table: users_user
```
**Fix**: Run migrations on backend:
```bash
python manage.py migrate
```

**4. Static Files Not Loading**
```
404 on /static/...
```
**Fix**: Run collectstatic:
```bash
python manage.py collectstatic --noinput
```

### Getting Help

- Check backend logs in hosting dashboard
- Use browser console (F12) for frontend errors
- Test API endpoints directly with curl/Postman
- Check environment variables are set correctly

---

## Next Steps

After deployment:

1. **Configure Payments**: Add real Stripe keys
2. **Set up Zoom**: Add Zoom SDK credentials for video sessions
3. **Email Configuration**: Set up SMTP for notifications
4. **Domain Setup**: Connect custom domain
5. **SSL Certificate**: Enable HTTPS (automatic on Render/Netlify)
6. **Monitoring**: Set up Sentry for error tracking
7. **Backups**: Configure database backups

---

## Security Checklist

Before going live:

- [ ] Change `SECRET_KEY` to random 50+ character string
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up HTTPS/SSL (automatic on most platforms)
- [ ] Enable CSRF protection
- [ ] Use environment variables for all secrets
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Review CORS settings
- [ ] Update Stripe to live keys (not test)
- [ ] Set up monitoring/logging

---

## Cost Estimation

### Free Tier (Good for testing)
- **Render**: Free tier (with limitations)
- **Netlify**: 100GB bandwidth/month free
- **Total**: $0/month

### Production Ready
- **Render Pro**: $7/month (backend)
- **Render PostgreSQL**: $7/month
- **Render Redis**: $10/month  
- **Netlify Pro**: $19/month (optional)
- **Domain**: $12/year
- **Total**: ~$25-45/month

---

## Conclusion

Your Motken platform is now deployed and accessible online! 🎉

**Access your app:**
- Frontend: `https://your-app.netlify.app`
- Backend API: `https://your-backend.onrender.com/api/v1/`
- Admin: `https://your-backend.onrender.com/admin/`

Test all features in the browser and share the URL with others for testing!
