# Deploy Motken to Your Netlify Account

## Step 1: Deploy Backend to Render (5 minutes)

### Why Backend First?
The Flutter app needs the backend API URL to connect to. Deploy backend first to get this URL.

### Backend Deployment:

1. **Go to Render**: https://render.com (sign up if needed)

2. **Create New Blueprint**:
   - Click "New +" → "Blueprint"
   - Connect your GitHub account
   - Select your `motken` repository
   - Render will detect `render.yaml` and show:
     - ✅ motken-backend (Web Service)
     - ✅ motken-db (PostgreSQL)
     - ✅ motken-redis (Redis)
     - ✅ motken-celery-worker (Worker)
     - ✅ motken-celery-beat (Worker)

3. **Click "Apply"** and wait 5-10 minutes

4. **Configure Environment Variables**:
   - Go to your `motken-backend` service
   - Click "Environment"
   - Add these variables:
     ```
     SECRET_KEY=your-random-50-character-secret-key-here
     ALLOWED_HOSTS=motken-backend.onrender.com
     CORS_ALLOWED_ORIGINS=https://YOUR_NETLIFY_URL.netlify.app
     ```
   - Note: You'll update `CORS_ALLOWED_ORIGINS` after getting your Netlify URL

5. **Get Your Backend URL**:
   - Example: `https://motken-backend.onrender.com`
   - Copy this URL - you'll need it for the frontend!

6. **Create Superuser** (Optional but recommended):
   - Go to backend service → "Shell"
   - Run: `python manage.py createsuperuser`
   - Follow prompts to create admin account

---

## Step 2: Deploy Frontend to Your Netlify Account (5 minutes)

### Option A: Deploy via Netlify Dashboard (Recommended)

1. **Go to Your Netlify Dashboard**:
   https://app.netlify.com/teams/hesham-sayed636/projects

2. **Add New Site**:
   - Click "Add new site" → "Import an existing project"

3. **Connect GitHub**:
   - Select "Deploy with GitHub"
   - Authorize Netlify to access your repositories
   - Select your `motken` repository

4. **Configure Build Settings**:
   ```
   Base directory: mobile
   Build command: flutter build web --release --dart-define=API_BASE_URL=https://YOUR_BACKEND_URL.onrender.com/api/v1/
   Publish directory: mobile/build/web
   ```

   **IMPORTANT**: Replace `YOUR_BACKEND_URL` with your actual Render backend URL!

   Example:
   ```
   Build command: flutter build web --release --dart-define=API_BASE_URL=https://motken-backend.onrender.com/api/v1/
   ```

5. **Add Environment Variables** (in Netlify):
   - Go to "Site settings" → "Environment variables"
   - Add:
     ```
     API_BASE_URL = https://motken-backend.onrender.com/api/v1/
     ```

6. **Deploy Settings** (auto-detected from netlify.toml):
   - Netlify will use the `netlify.toml` file we created
   - It handles SPA routing automatically
   - Sets up proper caching for assets

7. **Click "Deploy"**:
   - Wait 10-15 minutes for Flutter web build
   - Your app will be live at: `https://YOUR_APP.netlify.app`

8. **Update Backend CORS**:
   - Go back to Render backend
   - Update `CORS_ALLOWED_ORIGINS` with your Netlify URL:
     ```
     CORS_ALLOWED_ORIGINS=https://YOUR_APP.netlify.app
     ```
   - Redeploy backend for changes to take effect

---

### Option B: Deploy via Netlify CLI (Alternative)

If you prefer command line:

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to your account
netlify login

# Build the Flutter app
cd mobile
flutter build web --release \
  --dart-define=API_BASE_URL=https://YOUR_BACKEND_URL.onrender.com/api/v1/

# Deploy to your Netlify team
netlify deploy --prod \
  --dir=build/web \
  --site=YOUR_SITE_ID
```

---

## Step 3: Test Your Deployment (2 minutes)

### Test Backend
1. Visit: `https://YOUR_BACKEND.onrender.com/api/v1/health/`
   - Should return: `{"status": "ok"}`

2. Visit Admin: `https://YOUR_BACKEND.onrender.com/admin/`
   - Login with superuser credentials

3. Visit API Docs: `https://YOUR_BACKEND.onrender.com/api/schema/swagger-ui/`
   - Explore available endpoints

### Test Frontend
1. Visit your Netlify URL: `https://YOUR_APP.netlify.app`

2. **Test Registration**:
   - Click "Register"
   - Fill in form
   - Should create account successfully

3. **Test Login**:
   - Enter credentials
   - Should redirect to home page

4. **Test Teachers List**:
   - Navigate to Teachers
   - Should see data from backend (or empty state)

5. **Check Browser Console** (F12):
   - Look for API calls to your backend URL
   - Should see successful responses (200 status)

### Common Issues:

**CORS Error**:
```
Access to XMLHttpRequest blocked by CORS policy
```
**Fix**: Make sure `CORS_ALLOWED_ORIGINS` in backend includes your Netlify URL

**API Connection Failed**:
```
Network Error
```
**Fix**:
- Check backend is running on Render
- Verify API_BASE_URL in frontend build command
- Check browser console for exact error

**White Screen**:
- Check browser console for errors
- Make sure Flutter web build completed successfully
- Try clearing cache and hard reload (Ctrl+Shift+R)

---

## Step 4: Custom Domain (Optional)

### Add Custom Domain to Netlify:
1. Go to "Domain settings" in Netlify
2. Click "Add custom domain"
3. Follow DNS configuration instructions
4. Update backend `CORS_ALLOWED_ORIGINS` with your custom domain

---

## Environment Variables Reference

### Backend (Render):
```bash
# Required
DEBUG=False
SECRET_KEY=<random-50-char-string>
ALLOWED_HOSTS=motken-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-app.netlify.app

# Database (auto-configured by Render)
DATABASE_URL=<auto-set-by-render>

# Redis (auto-configured by Render)
REDIS_URL=<auto-set-by-render>

# Optional - Payment Integration
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key

# Optional - Video Integration
ZOOM_API_KEY=your_key
ZOOM_API_SECRET=your_secret
```

### Frontend (Netlify):
```bash
API_BASE_URL=https://motken-backend.onrender.com/api/v1/
```

---

## Troubleshooting

### Flutter Build Fails on Netlify

If the build fails, you have two options:

**Option 1: Build Locally and Deploy**
```bash
# Build on your machine
cd mobile
flutter build web --release \
  --dart-define=API_BASE_URL=https://YOUR_BACKEND_URL.onrender.com/api/v1/

# Manual deploy to Netlify
# Go to https://app.netlify.com/drop
# Drag and drop the 'build/web' folder
```

**Option 2: Use GitHub Actions to Build**
Create `.github/workflows/deploy.yml` (I can create this if needed)

---

## URLs After Deployment

After successful deployment, you'll have:

- **Frontend**: `https://your-app.netlify.app`
- **Backend API**: `https://motken-backend.onrender.com/api/v1/`
- **Admin Panel**: `https://motken-backend.onrender.com/admin/`
- **API Docs**: `https://motken-backend.onrender.com/api/schema/swagger-ui/`

---

## Cost

- **Render Free Tier**:
  - Backend with PostgreSQL and Redis
  - 750 hours/month (always on)
  - Spins down after inactivity

- **Netlify Free Tier**:
  - 100GB bandwidth/month
  - 300 build minutes/month
  - Automatic HTTPS

**Total: $0/month** ✅

---

## Next Steps After Deployment

1. **Create Sample Data**:
   - Login to admin panel
   - Create sample teachers
   - Create sample packages

2. **Test All Features**:
   - Registration/Login
   - Browse teachers
   - Book sessions
   - View packages
   - Profile management

3. **Share with Others**:
   - Share your Netlify URL
   - Others can test in browser
   - No installation needed!

4. **Configure Payments** (Optional):
   - Sign up for Stripe
   - Add Stripe keys to backend env vars
   - Test payment flow

5. **Set up Email** (Optional):
   - Configure SMTP settings
   - Enable email notifications

---

## Support

If you encounter any issues:
1. Check Render logs (in Render dashboard)
2. Check Netlify build logs (in Netlify dashboard)
3. Check browser console (F12) for frontend errors
4. Verify all environment variables are set correctly

---

## Quick Commands

### View Backend Logs on Render:
- Go to your service → "Logs" tab

### Redeploy Backend:
- Go to your service → "Manual Deploy" → "Deploy latest commit"

### Redeploy Frontend:
- Go to Netlify → "Deploys" → "Trigger deploy"

### Update Environment Variables:
- Render: Service → "Environment" → Edit → "Save Changes" → Redeploy
- Netlify: Site settings → "Environment variables" → Edit → Redeploy

---

Good luck with your deployment! 🚀
