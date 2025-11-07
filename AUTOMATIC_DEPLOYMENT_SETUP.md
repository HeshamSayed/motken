# 🚀 Automatic Deployment Setup

This guide will help you set up automatic deployment for the Motken app using GitHub Actions and Netlify.

## Overview

**What happens automatically:**
- ✅ Push code to GitHub → Backend auto-deploys to Render
- ✅ Push code to GitHub → Frontend auto-builds and deploys to Netlify
- ✅ No manual builds or deploys needed!
- ✅ Each push to main/master triggers automatic deployment

---

## Prerequisites

Before starting, you need:
- [ ] GitHub repository with your code
- [ ] Render account (for backend)
- [ ] Netlify account (for frontend)

---

## Part 1: Backend Automatic Deployment (Render)

### ✅ Already Configured!

The backend is already set up for automatic deployment via `render.yaml`.

### Steps:

1. **Push code to GitHub** (if not done already):
   ```bash
   git add .
   git commit -m "Setup automatic deployment"
   git push origin main
   ```

2. **Deploy to Render** (one-time setup):
   - Go to: https://render.com
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Select the `motken` repository
   - Click **"Apply"**
   - Wait 5-10 minutes for initial deployment

3. **Set Environment Variables** in Render:

   Go to each service and add these variables:

   **Backend Service (motken-backend)**:
   ```bash
   SECRET_KEY=<generate-random-50-char-string>
   DEBUG=False
   ALLOWED_HOSTS=<your-backend-url>.onrender.com
   CORS_ALLOWED_ORIGINS=https://timely-muffin-6841c8.netlify.app
   ```

   **Database and Redis** are auto-configured by Render!

4. **Get Your Backend URL**:
   - Copy from Render dashboard
   - Will look like: `https://motken-backend-abc123.onrender.com`
   - Save this - you'll need it for frontend setup

5. **Future Updates**:
   - Just push to GitHub
   - Render automatically detects changes and redeploys
   - Takes ~5 minutes per deploy

✅ **Backend automatic deployment is now active!**

---

## Part 2: Frontend Automatic Deployment (GitHub Actions + Netlify)

### Step 1: Get Netlify Credentials

You need two pieces of information from Netlify:

#### A) Get Netlify Auth Token

1. Go to: https://app.netlify.com/user/applications
2. Click **"New access token"**
3. Give it a name: "GitHub Actions Deploy"
4. Click **"Generate token"**
5. **Copy the token** (you'll only see it once!)
6. Save it securely - format: `nfp_abc123xyz...`

#### B) Get Netlify Site ID

You already have a site: `timely-muffin-6841c8`

1. Go to: https://app.netlify.com/sites/timely-muffin-6841c8/settings
2. Look for **"Site information"**
3. Find **"Site ID"**
4. **Copy the Site ID** (should be: `timely-muffin-6841c8` or a UUID)

### Step 2: Add Secrets to GitHub

1. **Go to your GitHub repository**:
   - Example: `https://github.com/YOUR_USERNAME/motken`

2. **Navigate to Settings**:
   - Click **"Settings"** tab (at the top)
   - Click **"Secrets and variables"** → **"Actions"** (in left sidebar)

3. **Add Secrets** - Click **"New repository secret"** for each:

   **Secret 1: NETLIFY_AUTH_TOKEN**
   ```
   Name: NETLIFY_AUTH_TOKEN
   Value: <paste your Netlify auth token>
   ```

   **Secret 2: NETLIFY_SITE_ID**
   ```
   Name: NETLIFY_SITE_ID
   Value: timely-muffin-6841c8
   ```

   **Secret 3: API_BASE_URL** (optional - has default)
   ```
   Name: API_BASE_URL
   Value: https://YOUR_BACKEND_URL.onrender.com/api/v1/
   ```

   Example: `https://motken-backend-abc123.onrender.com/api/v1/`

4. **Verify Secrets**:
   - You should see 3 secrets listed:
     - ✅ NETLIFY_AUTH_TOKEN
     - ✅ NETLIFY_SITE_ID
     - ✅ API_BASE_URL

### Step 3: Enable GitHub Actions

1. **Go to Actions Tab**:
   - In your GitHub repo, click **"Actions"** tab

2. **Enable Workflows**:
   - If you see "Workflows disabled", click **"Enable workflows"**

3. **Verify Workflow File**:
   - Check that `.github/workflows/deploy-frontend.yml` exists
   - It should be in your repository

### Step 4: Trigger First Deployment

**Option A: Push a change**
```bash
git add .
git commit -m "Enable automatic deployment"
git push origin main
```

**Option B: Manual trigger**
1. Go to **Actions** tab in GitHub
2. Click **"Deploy Frontend to Netlify"** workflow
3. Click **"Run workflow"** → **"Run workflow"**

### Step 5: Monitor Deployment

1. **Watch the workflow**:
   - Go to **Actions** tab
   - Click on the running workflow
   - Watch the build and deploy steps
   - Takes ~5-10 minutes

2. **Check Netlify**:
   - Go to: https://app.netlify.com/sites/timely-muffin-6841c8/deploys
   - You should see a new deploy from "GitHub Actions"

3. **Test Your Site**:
   - Visit: https://timely-muffin-6841c8.netlify.app
   - Should see the Motken login page!

✅ **Frontend automatic deployment is now active!**

---

## Part 3: Update Backend CORS

After frontend deploys successfully:

1. **Go to Render** → Your backend service
2. **Environment** → Find or add `CORS_ALLOWED_ORIGINS`
3. **Set value**:
   ```
   CORS_ALLOWED_ORIGINS=https://timely-muffin-6841c8.netlify.app
   ```
4. **Save Changes** → Backend will redeploy (~2 min)

---

## How It Works

### Automatic Deployment Flow:

```
1. You push code to GitHub
   ↓
2. GitHub Actions detects the push
   ↓
3. Workflow starts:
   - Installs Flutter
   - Builds web app with your backend API URL
   - Deploys to Netlify
   ↓
4. Your site is live!
   (Takes ~5-10 minutes)
```

### What Triggers Deployment:

✅ Push to `main` or `master` branch
✅ Changes in `mobile/` directory
✅ Changes in workflow file
✅ Manual trigger from Actions tab

❌ Changes only in `backend/` don't trigger frontend deploy
❌ Pull requests create preview (not production)

---

## Testing Automatic Deployment

### Test 1: Make a small change

```bash
# Edit something small in mobile app
echo "// test" >> mobile/lib/main.dart

# Commit and push
git add .
git commit -m "Test automatic deployment"
git push origin main
```

Watch in GitHub Actions to see it build and deploy!

### Test 2: Verify it works

1. Go to GitHub Actions tab
2. See "Deploy Frontend to Netlify" running
3. Wait for it to complete (green checkmark)
4. Visit your site: https://timely-muffin-6841c8.netlify.app
5. Hard refresh (Ctrl+Shift+R) to see changes

---

## Troubleshooting

### GitHub Actions fails with "Netlify token not found"

**Problem**: Secrets not set correctly

**Fix**:
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Verify `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` exist
3. Verify values are correct (no extra spaces)
4. Re-run the workflow

### Build succeeds but site shows old version

**Problem**: Browser cache

**Fix**:
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Or clear browser cache

### "CORS policy" error in browser

**Problem**: Backend doesn't allow your frontend URL

**Fix**:
1. Go to Render → Backend service → Environment
2. Update `CORS_ALLOWED_ORIGINS` to include:
   ```
   https://timely-muffin-6841c8.netlify.app
   ```
3. Make sure there's no trailing slash
4. Save and redeploy backend

### GitHub Actions shows "Flutter not found"

**Problem**: Flutter installation step failed

**Fix**:
- Check the workflow logs
- Usually fixes itself on retry
- Re-run the failed job

### Backend not deploying automatically

**Problem**: render.yaml not being detected

**Fix**:
1. Verify `render.yaml` is in repo root
2. In Render, go to Dashboard → Blueprint
3. Click "Sync" to refresh from Git

---

## Configuration Files

### GitHub Actions Workflow
**File**: `.github/workflows/deploy-frontend.yml`

This file:
- ✅ Installs Flutter 3.16.0
- ✅ Builds web app with your API URL
- ✅ Deploys to Netlify automatically
- ✅ Comments on PRs with deploy info

### Netlify Configuration
**File**: `mobile/netlify.toml`

This file:
- ✅ Sets publish directory
- ✅ Configures SPA routing
- ✅ Sets security headers
- ✅ Caches static assets

### Render Configuration
**File**: `render.yaml`

This file:
- ✅ Defines backend services
- ✅ Configures PostgreSQL database
- ✅ Sets up Redis
- ✅ Configures Celery workers

---

## Environment Variables Reference

### GitHub Secrets (Required)

| Secret Name | Description | Example |
|------------|-------------|---------|
| `NETLIFY_AUTH_TOKEN` | Netlify API token | `nfp_abc123xyz...` |
| `NETLIFY_SITE_ID` | Your Netlify site ID | `timely-muffin-6841c8` |
| `API_BASE_URL` | Backend API URL | `https://your-backend.onrender.com/api/v1/` |

### Render Environment Variables (Backend)

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Random 50+ chars |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `your-backend.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | CORS origins | `https://timely-muffin-6841c8.netlify.app` |
| `DATABASE_URL` | Database URL | Auto-set by Render |
| `REDIS_URL` | Redis URL | Auto-set by Render |

---

## Deployment Checklist

Before pushing to production:

### Backend (Render)
- [ ] Blueprint deployed successfully
- [ ] All environment variables set
- [ ] Database migrations run
- [ ] Superuser created (optional)
- [ ] Health check returns 200: `/api/v1/health/`
- [ ] API docs accessible: `/api/schema/swagger-ui/`

### Frontend (Netlify)
- [ ] GitHub secrets configured
- [ ] Workflow file exists
- [ ] First deployment successful
- [ ] Site loads correctly
- [ ] API connection works (check console)
- [ ] No CORS errors

### Integration
- [ ] Backend CORS includes frontend URL
- [ ] Frontend can reach backend API
- [ ] Login/register works
- [ ] Data loads from backend

---

## Updating Your App

### To deploy updates:

```bash
# Make your changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Add new feature"
git push origin main

# That's it! Both backend and frontend will auto-deploy
```

### Monitor deployments:

**Backend**: https://dashboard.render.com
**Frontend**: https://github.com/YOUR_USERNAME/motken/actions
**Site**: https://timely-muffin-6841c8.netlify.app

---

## Cost

**Total: $0/month** 🎉

- ✅ GitHub Actions: 2,000 minutes/month free
- ✅ Netlify: 300 build minutes/month free
- ✅ Render: Free tier with limitations
- ✅ All deployments covered by free tiers

---

## Advanced: Custom Domain (Optional)

### Add custom domain to Netlify:

1. Go to: https://app.netlify.com/sites/timely-muffin-6841c8/settings/domain
2. Click "Add custom domain"
3. Enter your domain: `www.yourapp.com`
4. Follow DNS configuration instructions
5. Update backend CORS to include new domain

---

## Support

### If something isn't working:

1. **Check GitHub Actions logs**:
   - Repo → Actions → Click on workflow run
   - Look for red X's and error messages

2. **Check Render logs**:
   - Render dashboard → Service → Logs tab

3. **Check Netlify logs**:
   - Netlify dashboard → Deploys → Click deploy → Logs

4. **Check browser console**:
   - Open site → Press F12 → Console tab
   - Look for errors

---

## Summary

You now have:
- ✅ Automatic backend deployment (Render Blueprint)
- ✅ Automatic frontend deployment (GitHub Actions + Netlify)
- ✅ No manual builds needed
- ✅ Push to GitHub = automatic deploy
- ✅ Takes ~5-10 minutes per deployment
- ✅ Completely free!

**Next time you want to deploy**: Just push to GitHub! 🚀
