# 🎯 Deploy Your App Now - Final Steps

Your repository is 100% ready! Just follow these 3 commands:

## Step 1: Merge Everything (1 minute)

```bash
# Create main branch if it doesn't exist
git checkout -b main 2>/dev/null || git checkout main

# Merge all deployment configurations
git merge claude/motken-quran-learning-app-011CUteokd56rfcFRQH4vKXz --no-edit

# Push to GitHub (this triggers automatic deployment!)
git push origin main
```

## Step 2: Add Secrets to GitHub (3 minutes)

**Go to**: `https://github.com/YOUR_USERNAME/motken/settings/secrets/actions`

Click **"New repository secret"** for each:

### Secret 1: NETLIFY_AUTH_TOKEN
1. Go to: https://app.netlify.com/user/applications
2. Click "New access token"
3. Name: "GitHub Actions"
4. Copy the token (starts with `nfp_`)
5. Paste in GitHub

### Secret 2: NETLIFY_SITE_ID
```
timely-muffin-6841c8
```

### Secret 3: API_BASE_URL (use this for now)
```
http://localhost:8000/api/v1/
```

## Step 3: Deploy Backend to Render (10 minutes)

1. **Open**: https://render.com
2. Click **"New +"** → **"Blueprint"**
3. **Connect GitHub** → Select `motken`
4. Click **"Apply"**
5. Wait 5-8 minutes

### Add Environment Variables in Render:
```bash
SECRET_KEY = <paste-random-50-char-string>
DEBUG = False
ALLOWED_HOSTS = your-backend-url.onrender.com
CORS_ALLOWED_ORIGINS = https://timely-muffin-6841c8.netlify.app
```

### Update API URL:
After backend deploys, update GitHub secret:
```
API_BASE_URL = https://YOUR_BACKEND_URL.onrender.com/api/v1/
```

Then redeploy: GitHub → Actions → "Deploy Frontend to Netlify" → "Run workflow"

---

## ✅ Your URLs

After deployment:
- Frontend: **https://timely-muffin-6841c8.netlify.app**
- Backend: **https://YOUR_BACKEND.onrender.com**

---

## 🎉 Done!

From now on, just push to deploy:
```bash
git push origin main
# Everything deploys automatically!
```
