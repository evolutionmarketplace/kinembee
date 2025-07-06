#!/bin/bash

# 🚀 Deploy Evolution Digital Market - Separated Frontend & Backend

echo "🎯 Deploying Evolution Digital Market with Separated Architecture"

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

# Step 1: Deploy Frontend to Vercel
print_info "Step 1: Deploying Frontend to Vercel..."

cd frontend

# Install Vercel CLI if not installed
if ! command -v vercel &> /dev/null; then
    print_info "Installing Vercel CLI..."
    npm install -g vercel
fi

# Build and deploy
print_info "Building frontend..."
npm install
npm run build

print_info "Deploying to Vercel..."
vercel --prod

cd ..

print_status "Frontend deployed to Vercel!"

# Step 2: Deploy Backend to Railway
print_info "Step 2: Setting up Backend for Railway..."

cd backend

# Create production requirements if not exists
if [ ! -f "requirements-production.txt" ]; then
    print_info "Creating production requirements..."
    cp requirements.txt requirements-production.txt
fi

cd ..

print_status "Backend ready for Railway deployment!"

print_info "Next steps:"
echo "1. Go to railway.app and connect your GitHub repository"
echo "2. Set root directory to 'backend'"
echo "3. Add environment variables:"
echo "   - SECRET_KEY=your-secret-key"
echo "   - DATABASE_URL=postgresql://... (Railway will provide)"
echo "   - ALLOWED_HOSTS=your-app.railway.app"
echo "   - CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app"
echo "4. Deploy!"

print_warning "Don't forget to:"
echo "1. Update VITE_API_URL in Vercel with your Railway backend URL"
echo "2. Update CORS_ALLOWED_ORIGINS in Railway with your Vercel frontend URL"

print_status "🎉 Deployment setup complete!"
echo ""
print_info "Your separated architecture is ready:"
echo "📱 Frontend: Vercel (React/TypeScript)"
echo "🔧 Backend: Railway (Django/Python)"
echo "🗄️  Database: Railway PostgreSQL"
echo ""
print_info "Total cost: $0/month with free tiers! 🚀"