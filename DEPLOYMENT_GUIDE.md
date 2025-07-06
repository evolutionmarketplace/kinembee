# 🚀 Deployment Guide - Evolution Digital Market

## Frontend Deployment (Vercel)

### Step 1: Fix Vercel Issues
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add: `VITE_API_URL` = `https://your-backend.railway.app`
5. Go to Settings → General
6. Set Build Command: `npm run build`
7. Set Output Directory: `dist`
8. Set Install Command: `npm install`
9. Set Node.js Version: `18.x`

### Step 2: Redeploy
1. Go to Deployments tab
2. Click "Redeploy" on the latest deployment
3. Or push a new commit to trigger deployment

## Backend Deployment (Railway)

### Step 1: Fix Railway Issues
1. Go to your Railway dashboard
2. Select your backend service
3. Go to Settings → Environment Variables
4. Add these variables:

```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key-here
ALLOWED_HOSTS=your-app.railway.app,localhost,127.0.0.1
DATABASE_URL=postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
DJANGO_SETTINGS_MODULE=evolution_market.settings.production
```

### Step 2: Deploy Backend
1. Go to Settings → General
2. Set Root Directory: `backend`
3. Set Start Command: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn evolution_market.wsgi:application --bind 0.0.0.0:$PORT`
4. Click "Deploy" or push a new commit

## Database Setup (Railway PostgreSQL)

### Option 1: Railway Database
1. In Railway, click "New" → "Database" → "PostgreSQL"
2. Copy the DATABASE_URL
3. Add it to your backend environment variables

### Option 2: Supabase (Free)
1. Go to supabase.com
2. Create new project
3. Get connection string from Settings → Database
4. Add as DATABASE_URL in Railway

## Troubleshooting

### Vercel Issues:
- **Build fails**: Check Node.js version is 18.x
- **No production deployment**: Ensure build command is `npm run build`
- **404 errors**: Check vercel.json routing configuration

### Railway Issues:
- **No deploys**: Check if root directory is set to `backend`
- **Build fails**: Ensure all environment variables are set
- **Database errors**: Check DATABASE_URL format

### Common Fixes:
1. **Clear build cache**: In Vercel/Railway settings
2. **Check logs**: View deployment logs for specific errors
3. **Environment variables**: Ensure all required vars are set
4. **Dependencies**: Check package.json and requirements.txt

## Quick Commands

### Redeploy Frontend:
```bash
# Push to trigger Vercel deployment
git add .
git commit -m "Fix deployment"
git push origin main
```

### Test Backend Locally:
```bash
cd backend
python manage.py runserver
```

### Check Frontend Build:
```bash
npm run build
npm run preview
```

## Environment Variables Checklist

### Frontend (Vercel):
- [ ] VITE_API_URL

### Backend (Railway):
- [ ] DEBUG=False
- [ ] SECRET_KEY
- [ ] ALLOWED_HOSTS
- [ ] DATABASE_URL
- [ ] CORS_ALLOWED_ORIGINS
- [ ] DJANGO_SETTINGS_MODULE

## Success URLs
- Frontend: `https://your-project.vercel.app`
- Backend: `https://your-backend.railway.app`
- Admin: `https://your-backend.railway.app/admin`

Your marketplace should be live once both deployments complete! 🎉