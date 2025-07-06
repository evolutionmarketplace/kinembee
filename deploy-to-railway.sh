#!/bin/bash

# 🚀 Deploy Evolution Digital Market Backend to Railway

echo "🚀 Deploying Evolution Digital Market Backend to Railway..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "backend/manage.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Navigate to backend directory
cd backend

print_info "Setting up backend for Railway deployment..."

# Create production requirements if not exists
if [ ! -f "requirements-production.txt" ]; then
    print_info "Creating production requirements..."
    cat > requirements-production.txt << 'EOF'
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-filter==23.3
django-environ==0.11.2
psycopg2-binary==2.9.7
dj-database-url==2.1.0
Pillow==10.0.1
celery==5.3.4
redis==5.0.1
django-redis==5.4.0
django-allauth==0.57.0
djangorestframework-simplejwt==5.3.0
stripe==7.8.0
sendgrid==6.10.0
gunicorn==21.2.0
whitenoise==6.6.0
sentry-sdk==1.38.0
django-ratelimit==4.1.0
django-cleanup==8.0.0
django-imagekit==5.0.0
django-taggit==4.0.0
django-mptt==0.15.0
channels==4.0.0
channels-redis==4.1.0
daphne==4.0.0
cloudinary==1.36.0
django-cloudinary-storage==0.3.0
EOF
fi

# Create Procfile
print_info "Creating Procfile..."
cat > Procfile << 'EOF'
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn evolution_market.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A evolution_market worker --loglevel=info
beat: celery -A evolution_market beat --loglevel=info
EOF

# Create runtime.txt
print_info "Creating runtime.txt..."
echo "python-3.11.0" > runtime.txt

# Create railway.json
print_info "Creating railway.json..."
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn evolution_market.wsgi:application --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/health/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

print_status "Backend setup complete!"

print_info "Next steps:"
echo "1. Go to https://railway.app"
echo "2. Click 'Deploy from GitHub repo'"
echo "3. Select your repository"
echo "4. Add these environment variables:"
echo "   - SECRET_KEY=your-secret-key"
echo "   - DATABASE_URL=postgresql://... (Railway will provide this)"
echo "   - ALLOWED_HOSTS=your-app.railway.app"
echo "   - CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app"
echo "   - DJANGO_SETTINGS_MODULE=evolution_market.settings.railway"
echo "5. Deploy!"

cd ..
print_status "Ready for Railway deployment! 🚀"