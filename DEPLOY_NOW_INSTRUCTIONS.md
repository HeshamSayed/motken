# 🚀 Deploy Now - Step-by-Step Instructions

Your repository is fully configured! Follow these steps to deploy your app.

---

## ✅ What's Ready

- ✅ GitHub Actions workflow configured
- ✅ Netlify configuration ready
- ✅ Render backend configuration ready
- ✅ All documentation created
- ✅ Deployment scripts prepared

---

## 🎯 Deploy in 3 Steps (15 minutes)

### Step 1: Merge to Main Branch (2 minutes)

You need to merge the deployment configuration to your main branch:

```bash
# Check out main branch (or master)
git checkout main

# Merge the deployment branch
git merge claude/motken-quran-learning-app-011CUteokd56rfcFRQH4vKXz

# Push to GitHub
git push origin main
```

⚠️ **This push will trigger GitHub Actions** to build and deploy your frontend!

---

### Step 2: Configure GitHub Secrets (3 minutes)

Before the build can complete, add these secrets:

1. **Go to your GitHub repository** on github.com

2. **Navigate to**: Settings → Secrets and variables → Actions

3. **Click "New repository secret"** and add each of these:

   **Secret 1: NETLIFY_AUTH_TOKEN**
   - Go to: https://app.netlify.com/user/applications
   - Click "New access token"
   - Name: "GitHub Actions Deploy"
   - Copy the token (starts with `nfp_...`)
   - Paste in GitHub secret value

   **Secret 2: NETLIFY_SITE_ID**
   ```
   Value: timely-muffin-6841c8
   ```

   **Secret 3: API_BASE_URL**
   ```
   Value: http://localhost:8000/api/v1/
   ```
   (You'll update this after deploying the backend)

4. **Trigger the workflow again** (if it already ran):
   - Go to Actions tab
   - Click "Deploy Frontend to Netlify"
   - Click "Run workflow"

---

### Step 3: Deploy Backend to Render (10 minutes)

While the frontend is building, deploy your backend:

1. **Go to**: https://render.com (sign up with GitHub)

2. **Create Blueprint**:
   - Click "New +" → "Blueprint"
   - Connect your GitHub account
   - Select your `motken` repository
   - Click "Apply"

3. **Wait for deployment** (~5-8 minutes)
   - Render will create:
     - ✅ Backend service (Django)
     - ✅ PostgreSQL database
     - ✅ Redis instance
     - ✅ Celery worker
     - ✅ Celery beat scheduler

4. **Get your backend URL**:
   - Go to the `motken-backend` service
   - Copy the URL (e.g., `https://motken-backend-abc123.onrender.com`)

5. **Configure Environment Variables**:
   - Click on `motken-backend` service
   - Go to "Environment" tab
   - Add these variables:

   ```bash
   SECRET_KEY = <generate a random 50-character string>
   DEBUG = False
   ALLOWED_HOSTS = motken-backend-abc123.onrender.com
   CORS_ALLOWED_ORIGINS = https://timely-muffin-6841c8.netlify.app
   ```

   To generate SECRET_KEY, you can use:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

   - Click "Save Changes"
   - Backend will redeploy (~2 minutes)

6. **Update GitHub Secret**:
   - Go back to GitHub → Settings → Secrets
   - Update `API_BASE_URL` to:
     ```
     https://YOUR_BACKEND_URL.onrender.com/api/v1/
     ```
   - Example: `https://motken-backend-abc123.onrender.com/api/v1/`

7. **Redeploy Frontend** (to pick up new API URL):
   - Go to GitHub → Actions
   - Click "Deploy Frontend to Netlify"
   - Click "Run workflow"

---

## ✅ Verify Deployment

### Check Backend:

```bash
curl https://YOUR_BACKEND_URL.onrender.com/api/v1/health/
```

Should return: `{"status": "ok"}`

### Check Frontend:

Visit: https://timely-muffin-6841c8.netlify.app

Should see: Motken login page!

### Test Integration:

1. Open your frontend URL
2. Press F12 (open developer console)
3. Go to Network tab
4. Try to register or login
5. Check for API calls to your backend
6. Should see successful 200 responses

---

## 🎉 You're Live!

After successful deployment:

### Your URLs:

| Service | URL |
|---------|-----|
| **Frontend** | https://timely-muffin-6841c8.netlify.app |
| **Backend API** | https://YOUR_BACKEND.onrender.com/api/v1/ |
| **Admin Panel** | https://YOUR_BACKEND.onrender.com/admin/ |
| **API Docs** | https://YOUR_BACKEND.onrender.com/api/schema/swagger-ui/ |

### Monitor Deployments:

- **GitHub Actions**: Your repo → Actions tab
- **Netlify**: https://app.netlify.com/sites/timely-muffin-6841c8/deploys
- **Render**: https://dashboard.render.com

---

## 🔄 Future Deployments

From now on, deployment is automatic:

```bash
# Make your changes
git add .
git commit -m "Add new feature"
git push origin main

# Both backend and frontend deploy automatically! 🚀
# Takes ~10 minutes
```

---

## 🐛 Troubleshooting

### GitHub Actions fails with "NETLIFY_AUTH_TOKEN not found"
→ Make sure you added all 3 secrets in GitHub Settings → Secrets

### Backend shows 502 or won't start
→ Check Render logs in the service dashboard
→ Verify environment variables are set correctly

### Frontend shows white screen
→ Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
→ Check browser console for errors

### CORS error when testing
→ Update `CORS_ALLOWED_ORIGINS` in Render backend to include your Netlify URL
→ Make sure there's no trailing slash

### "Can't connect to backend" error
→ Verify `API_BASE_URL` in GitHub secrets
→ Must end with `/api/v1/`
→ Backend must be running (check Render dashboard)

---

## 📚 More Help

- **Detailed guide**: [AUTOMATIC_DEPLOYMENT_SETUP.md](AUTOMATIC_DEPLOYMENT_SETUP.md)
- **Troubleshooting**: [TROUBLESHOOT_NETLIFY.md](TROUBLESHOOT_NETLIFY.md)
- **All options**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 💡 Alternative: Use the Deploy Script

If you prefer an interactive guide, run:

```bash
./deploy-now.sh
```

This script will walk you through each step with prompts.

---

## 📝 Deployment Checklist

Use this to track your progress:

- [ ] Merged deployment branch to main
- [ ] Pushed to GitHub
- [ ] Added NETLIFY_AUTH_TOKEN secret to GitHub
- [ ] Added NETLIFY_SITE_ID secret to GitHub
- [ ] Added API_BASE_URL secret to GitHub
- [ ] Deployed backend to Render via Blueprint
- [ ] Configured backend environment variables
- [ ] Updated API_BASE_URL with real backend URL
- [ ] Verified backend health check works
- [ ] Verified frontend loads
- [ ] Tested login/register functionality
- [ ] Confirmed API calls work (no CORS errors)

---

## 🎯 Quick Commands Reference

**Merge and deploy:**
```bash
git checkout main
git merge claude/motken-quran-learning-app-011CUteokd56rfcFRQH4vKXz
git push origin main
```

**Redeploy frontend manually:**
```bash
git commit --allow-empty -m "Redeploy frontend"
git push origin main
```

**Check GitHub Actions status:**
```bash
# View in browser: your-repo/actions
```

**Create admin user on Render:**
```bash
# In Render backend service → Shell tab:
python manage.py createsuperuser
```

---

**Ready to deploy? Start with Step 1!** 🚀

Good luck! Your app will be live in ~15 minutes.
