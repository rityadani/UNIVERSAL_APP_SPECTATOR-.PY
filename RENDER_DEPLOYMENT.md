# Render Deployment Guide

## Step-by-Step Render Deployment:

### 1. Go to Render.com
- Visit: https://render.com
- Sign up/Login with GitHub account

### 2. Connect GitHub Repository
- Click "New +" → "Web Service"
- Connect your GitHub account
- Select repository: `UNIVERSAL_APP_SPECTATOR-.PY`

### 3. Configure Deployment Settings
```
Name: universal-rl-dashboard
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python dashboard.py
```

### 4. Environment Variables (Optional)
```
PYTHON_VERSION = 3.11.0
PORT = 10000 (Render will set this automatically)
```

### 5. Deploy Settings
- Branch: main
- Auto-Deploy: Yes (recommended)
- Plan: Free (for testing)

### 6. Click "Create Web Service"

## Files Added for Render:
- ✅ `render.yaml` - Render configuration
- ✅ `runtime.txt` - Python version
- ✅ Updated `dashboard.py` - Port configuration
- ✅ `requirements.txt` - Dependencies

## After Deployment:
- Your dashboard will be live at: `https://your-app-name.onrender.com`
- Auto-deploys on every GitHub push
- Free tier includes 750 hours/month

## Troubleshooting:
- Check Render logs if deployment fails
- Ensure all files are pushed to GitHub
- Verify requirements.txt has all dependencies

## Expected URL:
`https://universal-rl-dashboard.onrender.com`

Your Universal RL Dashboard will be live on the internet! 🚀