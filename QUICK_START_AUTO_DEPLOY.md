# ⚡ Quick Start - Automatic Deployment

Get your Motken app deployed automatically in 3 steps!

---

## 🎯 What You'll Get

- ✅ **Automatic backend deployment** on Render
- ✅ **Automatic frontend deployment** on Netlify via GitHub Actions
- ✅ **No manual builds** - just push to GitHub!
- ✅ **Free** - uses all free tiers
- ✅ **Fast** - deploys in ~5-10 minutes

---

## 📋 Prerequisites

- [ ] GitHub repository (you have this!)
- [ ] Render account: https://render.com
- [ ] Netlify account: https://netlify.com
- [ ] Your repo pushed to GitHub

---

## 🚀 Step 1: Deploy Backend (8 minutes)

### 1.1 Deploy to Render

1. Go to: **https://render.com** (sign up with GitHub)
2. Click **"New +"** → **"Blueprint"**
3. Connect GitHub → Select your `motken` repository
4. Click **"Apply"** (detects `render.yaml` automatically)
5. Wait 5-8 minutes ⏱️

### 1.2 Configure Backend

1. Go to **motken-backend** service in Render
2. Click **"Environment"**
3. Add these variables:
   ```bash
   SECRET_KEY = <generate-random-50-character-string>
   DEBUG = False
   ALLOWED_HOSTS = motken-backend.onrender.com
   ```
4. Click **"Save Changes"** → Wait for redeploy (~2 min)

### 1.3 Get Backend URL

Your backend URL will be: `https://motken-backend-XXXX.onrender.com`

Copy this! You'll need it in the next step.

✅ **Backend is now deploying automatically on every push!**

---

## 🚀 Step 2: Setup Frontend Auto-Deploy (5 minutes)

### 2.1 Get Netlify Credentials

**A) Get Auth Token:**
1. Go to: https://app.netlify.com/user/applications
2. Click **"New access token"**
3. Name it: "GitHub Actions"
4. Click **"Generate token"**
5. **Copy the token** (`nfp_...`)

**B) Get Site ID:**
- Your site ID is: `timely-muffin-6841c8`
- Or get it from: https://app.netlify.com/sites/timely-muffin-6841c8/settings

### 2.2 Add Secrets to GitHub

1. Go to your repo: `https://github.com/YOUR_USERNAME/motken`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add each:

   **Secret 1:**
   ```
   Name: NETLIFY_AUTH_TOKEN
   Value: <paste your token from Netlify>
   ```

   **Secret 2:**
   ```
   Name: NETLIFY_SITE_ID
   Value: timely-muffin-6841c8
   ```

   **Secret 3:**
   ```
   Name: API_BASE_URL
   Value: https://YOUR_BACKEND_URL.onrender.com/api/v1/
   ```
   ⚠️ Replace `YOUR_BACKEND_URL` with your actual Render backend URL!

   Example: `https://motken-backend-abc123.onrender.com/api/v1/`

### 2.3 Enable GitHub Actions

1. Go to **Actions** tab in your repo
2. If disabled, click **"Enable workflows"**

✅ **Frontend auto-deploy is now configured!**

---

## 🚀 Step 3: Deploy! (2 minutes)

### 3.1 Trigger First Deployment

```bash
# Make sure all files are committed
git add .
git commit -m "Enable automatic deployment"
git push origin main
```

### 3.2 Watch It Deploy

1. Go to **Actions** tab in GitHub
2. See **"Deploy Frontend to Netlify"** running
3. Click on it to watch the build
4. Takes ~5-10 minutes ⏱️

### 3.3 Update Backend CORS

After frontend deploys:

1. Go to **Render** → Your backend service
2. **Environment** → Add or update:
   ```bash
   CORS_ALLOWED_ORIGINS = https://timely-muffin-6841c8.netlify.app
   ```
3. **Save** → Wait for redeploy (~2 min)

---

## ✅ Test Your Deployment

### Check Backend:
Open: `https://YOUR_BACKEND.onrender.com/api/v1/health/`

Should see: `{"status": "ok"}`

### Check Frontend:
Open: `https://timely-muffin-6841c8.netlify.app`

Should see: Motken login page!

### Test Connection:
1. Open your site
2. Press **F12** (open console)
3. Try to register/login
4. Check **Network** tab for API calls
5. Should see successful requests (200 OK)

---

## 🎉 You're Done!

### From now on:

```bash
# Just push to GitHub
git add .
git commit -m "Your changes"
git push origin main

# Both backend and frontend deploy automatically! 🚀
```

**Monitor deployments:**
- Backend: https://dashboard.render.com
- Frontend: https://github.com/YOUR_USERNAME/motken/actions
- Live site: https://timely-muffin-6841c8.netlify.app

---

## 🐛 Quick Troubleshooting

### GitHub Actions fails?
→ Check that all 3 secrets are set correctly in GitHub Settings → Secrets

### CORS error in browser?
→ Add your Netlify URL to `CORS_ALLOWED_ORIGINS` in Render backend

### Backend not responding?
→ Check Render dashboard - service should be green and running

### Site shows old version?
→ Hard refresh: **Ctrl+Shift+R** (Windows) or **Cmd+Shift+R** (Mac)

---

## 📚 Need More Help?

See detailed documentation:
- **`AUTOMATIC_DEPLOYMENT_SETUP.md`** - Complete setup guide
- **`TROUBLESHOOT_NETLIFY.md`** - Troubleshooting guide

---

## 💡 Key Points

✅ **Backend**: Push to GitHub → Render auto-deploys via `render.yaml`
✅ **Frontend**: Push to GitHub → Actions builds → Deploys to Netlify
✅ **Cost**: $0/month (all free tiers)
✅ **Time**: ~15 minutes initial setup, then automatic forever
✅ **Updates**: Just push to GitHub!

---

**Ready to deploy?** Follow the 3 steps above and you'll be live in 15 minutes! 🚀
