#!/bin/bash

# 🚀 Complete Deployment Script for Evolution Digital Market

echo "🎉 Complete Deployment of Evolution Digital Market"
echo "=================================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Make scripts executable
chmod +x deploy-to-railway.sh
chmod +x deploy-to-vercel.sh

print_info "Starting complete deployment process..."

# Step 1: Deploy Backend to Railway
print_info "Step 1: Setting up backend for Railway..."
./deploy-to-railway.sh

echo ""
print_warning "MANUAL STEP REQUIRED:"
echo "1. Go to https://railway.app"
echo "2. Sign up/login with GitHub"
echo "3. Click 'Deploy from GitHub repo'"
echo "4. Select your repository"
echo "5. Add environment variables (see .env.example)"
echo "6. Deploy the backend"
echo ""
read -p "Press Enter when backend is deployed and you have the Railway URL..."

# Step 2: Deploy Frontend to Vercel
print_info "Step 2: Deploying frontend to Vercel..."
./deploy-to-vercel.sh

echo ""
print_status "🎉 Deployment Complete!"
echo ""
print_info "Your Evolution Digital Market is now live!"
echo ""
echo "📱 Frontend: Check your Vercel dashboard for the URL"
echo "🔧 Backend: Check your Railway dashboard for the URL"
echo "🗄️  Database: Set up PostgreSQL in Railway or use Supabase"
echo ""
print_warning "Final Steps:"
echo "1. Update VITE_API_URL in Vercel with your Railway backend URL"
echo "2. Update CORS_ALLOWED_ORIGINS in Railway with your Vercel frontend URL"
echo "3. Set up your database (Railway PostgreSQL or Supabase)"
echo "4. Configure email (SendGrid), file storage (Cloudinary), and payments (Stripe)"
echo ""
print_status "Your marketplace is ready for users! 🚀"