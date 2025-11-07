# 🚀 Quick Deploy to Your Netlify Account

**Target**: https://app.netlify.com/teams/hesham-sayed636/projects

## ⚡ 2-Step Deployment (15 minutes total)

---

## Step 1: Deploy Backend (8 minutes)

### 1.1 Open Render
👉 Go to: https://render.com (sign up with GitHub)

### 1.2 Create Blueprint
1. Click **"New +"** → **"Blueprint"**
2. **Connect GitHub** → Select `motken` repository
3. Render detects `render.yaml` and shows 5 services:
   - ✅ motken-backend (Django API)
   - ✅ motken-db (PostgreSQL)
   - ✅ motken-redis (Redis)
   - ✅ motken-celery-worker
   - ✅ motken-celery-beat
4. Click **"Apply"**
5. Wait ~5 minutes ⏱️

### 1.3 Configure Backend
1. Go to **motken-backend** service
2. Click **"Environment"**
3. Add these variables:
   ```
   SECRET_KEY = django-insecure-CHANGE-THIS-TO-RANDOM-50-CHARS
   DEBUG = False
   ALLOWED_HOSTS = motken-backend.onrender.com
   ```
4. Click **"Save Changes"** → Backend will redeploy

### 1.4 Get Backend URL
📋 Copy your backend URL (will look like):
```
https://motken-backend-XXXX.onrender.com
```

💡 **Save this URL - you need it for the next step!**

---

## Step 2: Deploy Frontend to Your Netlify (7 minutes)

### 2.1 Open Your Netlify Dashboard
👉 Go to: https://app.netlify.com/teams/hesham-sayed636/projects

### 2.2 Add New Site
1. Click **"Add new site"** → **"Import an existing project"**

### 2.3 Connect GitHub
1. Select **"Deploy with GitHub"**
2. Authorize Netlify if needed
3. Select your **`motken`** repository

### 2.4 Configure Build (IMPORTANT!)
```
Base directory: mobile

Build command:
flutter config --enable-web && flutter pub get && flutter build web --release

Publish directory: mobile/build/web
```

### 2.5 Add Environment Variable (CRITICAL!)
Before clicking "Deploy", scroll down to **"Environment variables"**:

Click **"New variable"**:
```
Key:   API_BASE_URL
Value: https://YOUR_BACKEND_URL.onrender.com/api/v1/
```

**Example**:
```
Key:   API_BASE_URL
Value: https://motken-backend-abc123.onrender.com/api/v1/
```

⚠️ **Make sure to include `/api/v1/` at the end!**

### 2.6 Deploy!
1. Click **"Deploy site"**
2. Wait ~10-15 minutes ⏱️ (Flutter web build takes time)
3. Watch the build logs for progress

### 2.7 Get Your Frontend URL
📋 Your app will be live at:
```
https://YOUR_SITE_NAME.netlify.app
```

Example: `https://motken-quran-app.netlify.app`

---

## Step 3: Update Backend CORS (2 minutes)

### 3.1 Update Backend Environment
1. Go back to **Render** → **motken-backend** service
2. Click **"Environment"**
3. Find `CORS_ALLOWED_ORIGINS` variable (or add it)
4. Set to your Netlify URL:
   ```
   CORS_ALLOWED_ORIGINS = https://YOUR_SITE_NAME.netlify.app
   ```
5. Click **"Save Changes"**
6. Backend will redeploy (~2 minutes)

---

## ✅ Test Your Deployment

### Test 1: Backend Health
Open: `https://YOUR_BACKEND.onrender.com/api/v1/health/`

Should see:
```json
{"status": "ok"}
```

### Test 2: Frontend
Open: `https://YOUR_SITE_NAME.netlify.app`

Should see the Motken login page!

### Test 3: API Connection
1. Open browser console (Press F12)
2. Go to **Network** tab
3. Try to register/login
4. Check for API requests to your backend
5. Should see **200 OK** responses ✅

---

## 🎯 Your URLs

After deployment, you'll have:

| Service | URL |
|---------|-----|
| **Frontend** | `https://YOUR_SITE_NAME.netlify.app` |
| **Backend API** | `https://YOUR_BACKEND.onrender.com/api/v1/` |
| **Admin Panel** | `https://YOUR_BACKEND.onrender.com/admin/` |
| **API Docs** | `https://YOUR_BACKEND.onrender.com/api/schema/swagger-ui/` |

---

## 🐛 Troubleshooting

### Build Failed on Netlify?

**Solution 1: Check Build Logs**
- Go to Netlify → "Deploys" → Click on failed deploy
- Read the error message
- Usually missing Flutter SDK

**Solution 2: Build Locally & Upload**
```bash
cd mobile
flutter build web --release \
  --dart-define=API_BASE_URL=https://YOUR_BACKEND_URL.onrender.com/api/v1/

# Then go to: https://app.netlify.com/drop
# Drag and drop the 'build/web' folder
```

### CORS Error in Browser?

```
Access to XMLHttpRequest blocked by CORS policy
```

**Fix**:
1. Go to Render → motken-backend → Environment
2. Check `CORS_ALLOWED_ORIGINS` includes your Netlify URL
3. Must be exact: `https://your-site.netlify.app` (no trailing slash)
4. Save and redeploy

### Can't Connect to Backend?

**Check**:
1. Backend is running (green status in Render)
2. Backend URL is correct in Netlify env var
3. URL ends with `/api/v1/`
4. No typos in the URL

### White Screen on Frontend?

1. Check browser console for errors (F12)
2. Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
3. Check Netlify build logs for errors

---

## 💰 Cost

**Both are FREE!** 🎉

- ✅ Render Free Tier: Backend + Database + Redis
- ✅ Netlify Free Tier: 100GB bandwidth/month
- **Total: $0/month**

---

## 🎉 You're Done!

Share your app URL with anyone:
```
https://YOUR_SITE_NAME.netlify.app
```

They can test it in any browser - no installation needed!

---

## 📚 Need More Help?

See full documentation: `DEPLOY_TO_NETLIFY.md`

---

## 🔑 Quick Reference

### Environment Variables to Set

**Render (Backend)**:
```bash
SECRET_KEY=<random-50-chars>
DEBUG=False
ALLOWED_HOSTS=your-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-site.netlify.app
```

**Netlify (Frontend)**:
```bash
API_BASE_URL=https://your-backend.onrender.com/api/v1/
```

### Commands You Might Need

**View Backend Logs**:
Render Dashboard → Service → "Logs" tab

**Redeploy Backend**:
Render Dashboard → Service → "Manual Deploy" → "Deploy latest commit"

**Redeploy Frontend**:
Netlify Dashboard → "Deploys" → "Trigger deploy"

**Create Superuser** (for admin access):
Render Dashboard → Service → "Shell" tab:
```bash
python manage.py createsuperuser
```

---

Good luck! 🚀 Your app should be live in ~15 minutes!
