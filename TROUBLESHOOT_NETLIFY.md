# Troubleshooting Your Netlify Deployment

**Your Netlify Project**: https://app.netlify.com/projects/timely-muffin-6841c8/overview

## Common Issues & Solutions

### Issue 1: Build is Failing ❌

**Symptoms**:
- Netlify shows "Deploy failed" or "Build failed"
- Site doesn't deploy

**Check Build Logs**:
1. Go to: https://app.netlify.com/sites/timely-muffin-6841c8/deploys
2. Click on the latest (failed) deploy
3. Look at the build logs for errors

**Common Causes**:

#### A) Flutter Not Available
**Error**: `flutter: command not found`

**Solution**: Netlify's free tier may not support Flutter builds directly. Use local build instead:

```bash
# Build locally on your machine
cd mobile
flutter build web --release \
  --dart-define=API_BASE_URL=https://YOUR_BACKEND_URL.onrender.com/api/v1/

# Then deploy manually:
# 1. Go to https://app.netlify.com/drop
# 2. Drag and drop the 'mobile/build/web' folder
# 3. Your site will deploy instantly!
```

#### B) Base Directory Issue
**Error**: `Could not find mobile/ directory`

**Fix in Netlify**:
1. Site settings → Build & deploy → Build settings
2. Set **Base directory**: `mobile`
3. Set **Publish directory**: `mobile/build/web`

---

### Issue 2: Site Loads But Shows White Screen 🤍

**Symptoms**:
- Site deploys successfully
- But shows blank white page

**Solutions**:

#### Check Browser Console:
1. Press `F12` (or right-click → Inspect)
2. Go to **Console** tab
3. Look for errors (usually red text)

**Common Errors**:

**A) "Failed to load canvaskit.wasm"**
```
Fix: This is normal on first load. Hard refresh:
- Windows: Ctrl + Shift + R
- Mac: Cmd + Shift + R
```

**B) "Uncaught (in promise) TypeError"**
```
Fix: Check if API_BASE_URL is set correctly in build
```

---

### Issue 3: Can't Connect to Backend API ❌

**Symptoms**:
- Site loads
- Login/Register doesn't work
- Console shows network errors

**Check These**:

#### A) Verify Backend is Running
Open: `https://YOUR_BACKEND_URL.onrender.com/api/v1/health/`

Should return: `{"status": "ok"}`

If backend shows error or doesn't load:
- Go to Render dashboard
- Check backend service status (should be green)
- Check logs for errors

#### B) Check API_BASE_URL Environment Variable

In Netlify:
1. Site settings → Environment variables
2. Look for `API_BASE_URL`
3. Should be: `https://YOUR_BACKEND_URL.onrender.com/api/v1/`
4. ⚠️ Must end with `/api/v1/`

If missing or wrong:
1. Add/update the variable
2. Trigger new deploy: Deploys → "Trigger deploy" → "Deploy site"

#### C) CORS Error in Browser Console

**Error**:
```
Access to XMLHttpRequest at 'https://...' from origin 'https://timely-muffin-6841c8.netlify.app'
has been blocked by CORS policy
```

**Fix**:
1. Go to **Render** → Your backend service
2. Environment → Find `CORS_ALLOWED_ORIGINS`
3. Set to: `https://timely-muffin-6841c8.netlify.app`
4. Save → Backend will redeploy
5. Wait 2-3 minutes
6. Try again

---

### Issue 4: Build Takes Too Long / Times Out ⏱️

**Symptoms**:
- Build runs for 15+ minutes
- Build times out

**Solution**: Build locally and deploy manually

```bash
# On your machine:
cd mobile

# Make sure Flutter is installed
flutter --version

# Build
flutter build web --release \
  --dart-define=API_BASE_URL=https://YOUR_BACKEND_URL.onrender.com/api/v1/

# The build/web folder is ready to deploy!
```

**Deploy to Netlify**:
1. Go to: https://app.netlify.com/drop
2. Drag the `mobile/build/web` folder
3. Drop it on the page
4. ✅ Instant deploy!

Or connect to your existing site:
1. Go to: https://app.netlify.com/sites/timely-muffin-6841c8/deploys
2. Scroll down → "Need to deploy manually?"
3. Drag the `mobile/build/web` folder

---

## Quick Diagnostic Checklist

Run through this checklist:

### Backend (Render)
- [ ] Backend service is running (green status)
- [ ] Can access: `https://YOUR_BACKEND.onrender.com/api/v1/health/`
- [ ] `CORS_ALLOWED_ORIGINS` includes: `https://timely-muffin-6841c8.netlify.app`
- [ ] Database is connected
- [ ] Environment variables are set

### Frontend (Netlify)
- [ ] Build completed successfully
- [ ] Site is published
- [ ] Can access: `https://timely-muffin-6841c8.netlify.app`
- [ ] `API_BASE_URL` environment variable is set
- [ ] Points to correct backend URL with `/api/v1/`

### Test Connection
- [ ] Open site in browser
- [ ] Open console (F12)
- [ ] Try to login/register
- [ ] Check network tab for API calls
- [ ] Should see requests to your backend
- [ ] Should get 200 responses (not 404, 500, or CORS errors)

---

## Alternative: Simple Local Build + Manual Deploy

**This is the most reliable method for Netlify free tier:**

### Step 1: Build Locally
```bash
cd mobile

# Configure API URL (replace with your actual backend URL)
flutter build web --release \
  --dart-define=API_BASE_URL=https://motken-backend-xyz.onrender.com/api/v1/

# Wait for build to complete (2-5 minutes)
# Output: mobile/build/web
```

### Step 2: Deploy to Netlify
1. **Go to**: https://app.netlify.com/drop
2. **Drag and drop** the `mobile/build/web` folder
3. **Done!** Your site deploys in seconds

### Step 3: Connect to Your Project
After deploy, Netlify gives you a URL. To connect to your project:
1. Copy the deploy URL
2. Go to: https://app.netlify.com/sites/timely-muffin-6841c8/settings
3. Site details → "Change site name"
4. Or claim the existing site

---

## Get Specific Help

To help you better, please tell me:

1. **What exactly is happening?**
   - [ ] Build is failing
   - [ ] Site shows white screen
   - [ ] Can't connect to backend
   - [ ] Login/Register not working
   - [ ] Other: ___________

2. **What do you see in browser console?** (Press F12)
   - Copy any error messages

3. **What do you see in Netlify build logs?**
   - Go to Deploys → Click latest deploy → Copy error

4. **Is your backend running?**
   - Visit: `https://YOUR_BACKEND.onrender.com/api/v1/health/`
   - What do you see?

---

## Quick Fixes by Error Type

### "Failed to fetch" or "Network Error"
→ Backend is down or wrong URL
→ Check backend status on Render
→ Verify API_BASE_URL environment variable

### "CORS policy" error
→ Backend doesn't allow your frontend URL
→ Add Netlify URL to CORS_ALLOWED_ORIGINS in backend

### "404 Not Found" on API calls
→ API_BASE_URL is wrong
→ Should end with `/api/v1/`

### White screen, no errors
→ Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
→ Clear cache and reload

### Build timeout
→ Use local build method (see above)
→ Deploy build/web folder manually

---

## Recommended Approach (Easiest)

1. **Deploy Backend to Render** (if not done):
   - Use the blueprint method from previous guide
   - Get backend URL

2. **Build Flutter App Locally**:
   ```bash
   cd mobile
   flutter build web --release \
     --dart-define=API_BASE_URL=https://YOUR_BACKEND.onrender.com/api/v1/
   ```

3. **Deploy to Netlify via Drag & Drop**:
   - Go to: https://app.netlify.com/drop
   - Drag `mobile/build/web` folder
   - Get instant deploy

4. **Update Backend CORS**:
   - Add your Netlify URL to backend CORS settings

This bypasses all build issues and gets you deployed in minutes!

---

## Still Stuck?

Share these details:
1. Error message from Netlify build logs
2. Error message from browser console (F12)
3. Your backend URL (if deployed)
4. Screenshot of the issue

I'll help you fix it! 🚀
