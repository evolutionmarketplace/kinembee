#!/bin/bash

# 🚀 Evolution Digital Market - Free Deployment Script

echo "🎯 Starting Free Deployment Process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if required tools are installed
check_requirements() {
    print_info "Checking requirements..."
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    print_status "All requirements met!"
}

# Install deployment tools
install_tools() {
    print_info "Installing deployment tools..."
    
    # Install Vercel CLI
    npm install -g vercel
    
    # Install Netlify CLI
    npm install -g netlify-cli
    
    print_status "Deployment tools installed!"
}

# Build frontend
build_frontend() {
    print_info "Building frontend for production..."
    
    # Install dependencies
    npm install
    
    # Build for production
    npm run build
    
    print_status "Frontend built successfully!"
}

# Deploy to Vercel
deploy_vercel() {
    print_info "Deploying to Vercel..."
    
    # Deploy to Vercel
    vercel --prod
    
    print_status "Deployed to Vercel!"
}

# Deploy to Netlify
deploy_netlify() {
    print_info "Deploying to Netlify..."
    
    # Deploy to Netlify
    netlify deploy --prod --dir=dist
    
    print_status "Deployed to Netlify!"
}

# Deploy to GitHub Pages
deploy_github_pages() {
    print_info "Deploying to GitHub Pages..."
    
    # Install gh-pages
    npm install --save-dev gh-pages
    
    # Add deploy script to package.json if not exists
    if ! grep -q '"deploy"' package.json; then
        npm pkg set scripts.deploy="gh-pages -d dist"
    fi
    
    # Deploy
    npm run deploy
    
    print_status "Deployed to GitHub Pages!"
}

# Setup backend for deployment
setup_backend() {
    print_info "Setting up backend for deployment..."
    
    cd backend
    
    # Create production requirements
    if [ ! -f "requirements-production.txt" ]; then
        pip freeze > requirements-production.txt
    fi
    
    # Create Procfile if not exists
    if [ ! -f "Procfile" ]; then
        echo "web: gunicorn evolution_market.wsgi:application --bind 0.0.0.0:\$PORT" > Procfile
    fi
    
    # Create runtime.txt if not exists
    if [ ! -f "runtime.txt" ]; then
        echo "python-3.11.0" > runtime.txt
    fi
    
    cd ..
    
    print_status "Backend setup complete!"
}

# Main deployment menu
main_menu() {
    echo ""
    echo "🚀 Evolution Digital Market - Free Deployment"
    echo "=============================================="
    echo ""
    echo "Choose your deployment option:"
    echo ""
    echo "Frontend Options:"
    echo "1) Deploy to Vercel (Recommended)"
    echo "2) Deploy to Netlify"
    echo "3) Deploy to GitHub Pages"
    echo ""
    echo "Backend Options:"
    echo "4) Setup for Railway deployment"
    echo "5) Setup for Render deployment"
    echo "6) Setup for Heroku deployment"
    echo ""
    echo "Complete Setup:"
    echo "7) Full deployment guide"
    echo "8) Exit"
    echo ""
    read -p "Enter your choice (1-8): " choice
    
    case $choice in
        1)
            build_frontend
            deploy_vercel
            ;;
        2)
            build_frontend
            deploy_netlify
            ;;
        3)
            build_frontend
            deploy_github_pages
            ;;
        4)
            setup_backend
            print_info "Backend ready for Railway! Go to railway.app and deploy."
            ;;
        5)
            setup_backend
            print_info "Backend ready for Render! Go to render.com and deploy."
            ;;
        6)
            setup_backend
            print_info "Backend ready for Heroku! Use 'git push heroku main' to deploy."
            ;;
        7)
            show_deployment_guide
            ;;
        8)
            print_info "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid option. Please try again."
            main_menu
            ;;
    esac
}

# Show complete deployment guide
show_deployment_guide() {
    echo ""
    echo "📋 Complete Free Deployment Guide"
    echo "=================================="
    echo ""
    echo "🎯 Recommended Free Stack:"
    echo "• Frontend: Vercel (React/Vite)"
    echo "• Backend: Railway (Django)"
    echo "• Database: Supabase PostgreSQL"
    echo "• File Storage: Cloudinary"
    echo "• Email: SendGrid"
    echo ""
    echo "💰 Total Cost: \$0/month"
    echo ""
    echo "🔗 Quick Links:"
    echo "• Vercel: https://vercel.com"
    echo "• Railway: https://railway.app"
    echo "• Supabase: https://supabase.com"
    echo "• Cloudinary: https://cloudinary.com"
    echo "• SendGrid: https://sendgrid.com"
    echo ""
    echo "📖 Full guide available in deploy-free.md"
    echo ""
}

# Start deployment process
echo "🎉 Welcome to Evolution Digital Market Free Deployment!"
echo ""

check_requirements
install_tools
main_menu

print_status "Deployment process completed!"
print_info "Your marketplace is now live and ready for users! 🚀"