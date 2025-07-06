#!/bin/bash

# 🚀 Deploy Evolution Digital Market Frontend to Vercel

echo "🚀 Deploying Evolution Digital Market Frontend to Vercel..."

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
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

print_info "Setting up frontend for Vercel deployment..."

# Install Vercel CLI if not installed
if ! command -v vercel &> /dev/null; then
    print_info "Installing Vercel CLI..."
    npm install -g vercel
fi

# Create vercel.json if not exists
if [ ! -f "vercel.json" ]; then
    print_info "Creating vercel.json..."
    cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "VITE_API_URL": "@vite_api_url"
  }
}
EOF
fi

# Install dependencies
print_info "Installing dependencies..."
npm install

# Build for production
print_info "Building for production..."
npm run build

# Deploy to Vercel
print_info "Deploying to Vercel..."
vercel --prod

print_status "Frontend deployed to Vercel! 🚀"

print_info "Don't forget to:"
echo "1. Set VITE_API_URL environment variable in Vercel dashboard"
echo "2. Point it to your Railway backend URL"
echo "3. Update CORS_ALLOWED_ORIGINS in your backend with the Vercel URL"