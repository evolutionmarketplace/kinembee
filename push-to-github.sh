#!/bin/bash

# 🚀 Automated GitHub Setup and Push Script for Evolution Digital Market

echo "🎯 Setting up GitHub repository for Evolution Digital Market..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_header() {
    echo -e "${PURPLE}🚀 $1${NC}"
}

# Check if git is installed
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        echo "Visit: https://git-scm.com/downloads"
        exit 1
    fi
    print_status "Git is installed"
}

# Check if GitHub CLI is installed
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        print_warning "GitHub CLI is not installed. We'll use manual setup."
        return 1
    fi
    print_status "GitHub CLI is installed"
    return 0
}

# Get repository information
get_repo_info() {
    echo ""
    print_header "Repository Setup"
    echo "Let's set up your GitHub repository!"
    echo ""
    
    # Use provided username or ask for it
    GITHUB_USERNAME="evolution254"
    echo "Using GitHub username: $GITHUB_USERNAME"
    
    read -p "Enter repository name (default: evolution-digital-market): " REPO_NAME
    REPO_NAME=${REPO_NAME:-evolution-digital-market}
    
    read -p "Make repository private? (y/N): " PRIVATE_REPO
    PRIVATE_REPO=${PRIVATE_REPO:-n}
    
    echo ""
    print_info "Repository details:"
    echo "  Username: $GITHUB_USERNAME"
    echo "  Repository: $REPO_NAME"
    echo "  Private: $PRIVATE_REPO"
    echo ""
}

# Initialize git repository
init_git() {
    print_info "Initializing Git repository..."
    
    # Initialize git if not already initialized
    if [ ! -d ".git" ]; then
        git init
        print_status "Git repository initialized"
    else
        print_status "Git repository already exists"
    fi
    
    # Set up git config if not set
    if [ -z "$(git config user.name)" ]; then
        git config user.name "Evolution254"
        print_status "Git username set to Evolution254"
    fi
    
    if [ -z "$(git config user.email)" ]; then
        read -p "Enter your Git email: " GIT_EMAIL
        git config user.email "$GIT_EMAIL"
        print_status "Git email configured"
    fi
    
    print_status "Git configuration complete"
}

# Create .gitignore file
create_gitignore() {
    print_info "Creating comprehensive .gitignore..."
    
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Build outputs
dist/
dist-ssr/
*.local

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea/
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output/

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/

# Deployment
.vercel
.netlify

# Local Netlify folder
.netlify
EOF

    print_status ".gitignore created"
}

# Create README.md
create_readme() {
    print_info "Creating comprehensive README.md..."
    
    cat > README.md << 'EOF'
# 🚀 Evolution Digital Market

A modern, full-stack peer-to-peer marketplace built with React, Django, and cutting-edge technologies.

![Evolution Market](https://images.pexels.com/photos/230544/pexels-photo-230544.jpeg?auto=compress&cs=tinysrgb&w=1200)

## ✨ Features

### 🎯 Core Marketplace Features
- **User Authentication** - Secure registration, login, and profile management
- **Product Listings** - Create, edit, and manage product listings with multiple images
- **Advanced Search & Filters** - Find products by category, price, location, and condition
- **Real-time Chat** - Instant messaging between buyers and sellers
- **Price Negotiations** - Make and respond to price offers
- **Reviews & Ratings** - Build trust with user feedback system
- **Wishlist & Favorites** - Save products for later
- **Product Comparison** - Compare up to 4 products side-by-side

### 💳 Payment & Monetization
- **Stripe Integration** - Secure payment processing
- **Boost Listings** - Premium placement for better visibility
- **Commission System** - Platform revenue through transaction fees
- **Wallet System** - Manage earnings and payouts

### 📱 User Experience
- **Mobile Responsive** - Perfect experience on all devices
- **Progressive Web App** - App-like experience in browsers
- **Real-time Notifications** - Stay updated with instant alerts
- **Advanced Filters** - Powerful search and filtering options
- **Recently Viewed** - Track browsing history
- **Saved Searches** - Get alerts for new matching products

### 🛡️ Trust & Safety
- **User Verification** - Email and phone verification
- **Report System** - Flag inappropriate content
- **Block Users** - Prevent unwanted communications
- **Admin Dashboard** - Comprehensive moderation tools
- **Secure Transactions** - Protected payment processing

## 🏗️ Tech Stack

### Frontend
- **React 18** - Modern UI library with hooks
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vite** - Lightning-fast build tool
- **Lucide React** - Beautiful icons

### Backend
- **Django 4.2** - Robust Python web framework
- **Django REST Framework** - Powerful API development
- **PostgreSQL** - Reliable database
- **Redis** - Caching and real-time features
- **Celery** - Background task processing
- **Channels** - WebSocket support for real-time chat

### Infrastructure & Services
- **Vercel** - Frontend deployment
- **Railway** - Backend deployment
- **Supabase** - Database hosting
- **Cloudinary** - Image storage and optimization
- **Resend** - Email delivery service
- **Stripe** - Payment processing

## 🚀 Quick Start

### Prerequisites
- Node.js 20+ and npm
- Python 3.11+
- PostgreSQL
- Redis (optional, for caching)

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## 🌐 Free Deployment

Deploy your entire marketplace for **$0/month** using our free tier setup:

```bash
# Quick deploy script
chmod +x deploy-complete.sh
./deploy-complete.sh
```

**Free Services Used:**
- **Vercel** - Frontend hosting (Free)
- **Railway** - Backend hosting ($5 free credit/month)
- **Supabase** - PostgreSQL database (Free tier)
- **Cloudinary** - Image storage (Free tier)
- **Resend** - Email service (3,000 emails/month free)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📊 Project Structure

```
evolution-digital-market/
├── src/                    # Frontend React app
│   ├── components/         # Reusable UI components
│   ├── context/           # React context providers
│   ├── hooks/             # Custom React hooks
│   ├── types/             # TypeScript type definitions
│   └── data/              # Mock data and constants
├── backend/               # Django backend
│   ├── apps/              # Django applications
│   │   ├── accounts/      # User management
│   │   ├── products/      # Product listings
│   │   ├── categories/    # Product categories
│   │   ├── reviews/       # Review system
│   │   ├── chat/          # Real-time messaging
│   │   ├── payments/      # Payment processing
│   │   └── notifications/ # Notification system
│   └── evolution_market/  # Django project settings
└── docs/                  # Documentation
```

## 🔧 Configuration

### Environment Variables

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

#### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
RESEND_API_KEY=your-resend-api-key
STRIPE_SECRET_KEY=sk_test_your-stripe-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
```

## 🎨 Design System

### Colors
- **Primary**: Blue (#3B82F6)
- **Secondary**: Emerald (#10B981)
- **Accent**: Purple (#8B5CF6)
- **Success**: Green (#22C55E)
- **Warning**: Yellow (#F59E0B)
- **Error**: Red (#EF4444)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📝 API Documentation

The API is built with Django REST Framework and includes:

- **Authentication**: JWT-based auth with refresh tokens
- **Products**: CRUD operations with advanced filtering
- **Chat**: Real-time messaging with WebSocket support
- **Payments**: Stripe integration for secure transactions
- **Notifications**: Real-time alerts and email notifications

## 🔒 Security

- **HTTPS Everywhere** - All communications encrypted
- **JWT Authentication** - Secure token-based auth
- **Input Validation** - Comprehensive data validation
- **CORS Protection** - Proper cross-origin configuration
- **Rate Limiting** - API abuse prevention

## 📈 Performance

- **Optimized Images** - Automatic compression and WebP conversion
- **Lazy Loading** - Images and components load on demand
- **Code Splitting** - Reduced bundle sizes
- **Caching** - Redis-powered caching layer
- **CDN** - Global content delivery

## 📱 Mobile Support

The marketplace is fully responsive and works perfectly on mobile devices. PWA features provide an app-like experience.

## 🌍 Internationalization

The platform supports multiple languages and currencies:
- English (default)
- Spanish
- French
- German

## 📊 Analytics

Built-in analytics track:
- User engagement
- Product performance
- Sales metrics
- Search patterns
- Conversion rates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **React Team** - For the amazing React library
- **Django Team** - For the robust Django framework
- **Tailwind CSS** - For the utility-first CSS framework
- **Stripe** - For secure payment processing
- **Vercel** - For excellent hosting platform

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/evolution254/evolution-digital-market/issues)
- **Discussions**: [GitHub Discussions](https://github.com/evolution254/evolution-digital-market/discussions)

---

**Built with ❤️ by Evolution254**

[🌟 Star us on GitHub](https://github.com/evolution254/evolution-digital-market) | [🚀 Live Demo](https://evolution-market.vercel.app)
EOF

    print_status "README.md created"
}

# Create LICENSE file
create_license() {
    print_info "Creating MIT LICENSE..."
    
    cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Evolution254

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

    print_status "LICENSE created"
}

# Create GitHub repository using CLI
create_repo_with_cli() {
    print_info "Creating GitHub repository with CLI..."
    
    if [ "$PRIVATE_REPO" = "y" ] || [ "$PRIVATE_REPO" = "Y" ]; then
        gh repo create "$REPO_NAME" --private --description "🚀 Evolution Digital Market - Modern P2P Marketplace Platform with React, Django, and real-time features. Deploy for free!"
    else
        gh repo create "$REPO_NAME" --public --description "🚀 Evolution Digital Market - Modern P2P Marketplace Platform with React, Django, and real-time features. Deploy for free!"
    fi
    
    if [ $? -eq 0 ]; then
        print_status "GitHub repository created successfully"
        REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        return 0
    else
        print_error "Failed to create repository with CLI"
        return 1
    fi
}

# Manual repository creation instructions
manual_repo_creation() {
    print_warning "Manual repository creation required"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Description: 🚀 Evolution Digital Market - Modern P2P Marketplace Platform"
    if [ "$PRIVATE_REPO" = "y" ] || [ "$PRIVATE_REPO" = "Y" ]; then
        echo "4. Make it Private"
    else
        echo "4. Make it Public"
    fi
    echo "5. Don't initialize with README, .gitignore, or license"
    echo "6. Click 'Create repository'"
    echo ""
    read -p "Press Enter when you've created the repository..."
    
    REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
}

# Add files to git
add_files() {
    print_info "Adding files to Git..."
    
    # Add all files except those in .gitignore
    git add .
    
    # Check if there are any changes to commit
    if git diff --staged --quiet; then
        print_warning "No changes to commit"
        return 1
    fi
    
    print_status "Files added to Git"
    return 0
}

# Create initial commit
create_commit() {
    print_info "Creating initial commit..."
    
    git commit -m "🚀 Initial commit: Evolution Digital Market

✨ Features:
- Modern React + TypeScript frontend with Tailwind CSS
- Django REST API backend with comprehensive apps
- Real-time chat system with WebSocket support
- Payment processing with Stripe integration
- User authentication & profile management
- Product listings with advanced search & filters
- Review & rating system for trust building
- Admin dashboard for platform management
- Mobile responsive PWA design
- Email notifications with Resend
- File storage with Cloudinary
- Free deployment ready (Vercel + Railway)

🎯 Production-ready marketplace platform!
🌟 Deploy for \$0/month with included free tier setup
📱 Mobile-first responsive design
🔒 Security-focused with JWT auth & input validation
⚡ Performance optimized with caching & CDN
🌍 Internationalization support

Built with ❤️ by Evolution254
Ready to revolutionize P2P marketplaces! 🚀"

    if [ $? -eq 0 ]; then
        print_status "Initial commit created"
        return 0
    else
        print_error "Failed to create commit"
        return 1
    fi
}

# Add remote and push
push_to_github() {
    print_info "Setting up remote and pushing to GitHub..."
    
    # Add remote origin
    git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
    
    # Set default branch to main
    git branch -M main
    
    # Push to GitHub
    print_info "Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        print_status "Successfully pushed to GitHub!"
        return 0
    else
        print_error "Failed to push to GitHub"
        print_info "You may need to authenticate with GitHub"
        print_info "Try: gh auth login"
        return 1
    fi
}

# Create GitHub community files
create_github_files() {
    print_info "Creating GitHub community files..."
    
    # Create .github directory
    mkdir -p .github/ISSUE_TEMPLATE
    
    # Bug report template
    cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. iOS, Windows, macOS]
 - Browser [e.g. chrome, safari, firefox]
 - Version [e.g. 22]

**Additional context**
Add any other context about the problem here.
EOF

    # Feature request template
    cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
EOF

    # Pull request template
    cat > .github/pull_request_template.md << 'EOF'
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally with my changes
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Manual testing completed

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] Any dependent changes have been merged and published in downstream modules
EOF

    # Contributing guide
    cat > CONTRIBUTING.md << 'EOF'
# Contributing to Evolution Digital Market

Thank you for your interest in contributing to Evolution Digital Market! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/evolution-digital-market.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m 'Add some amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Submit a pull request

## Development Setup

### Frontend
```bash
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Code Style

### Frontend
- Use TypeScript for all new code
- Follow React best practices and hooks patterns
- Use Tailwind CSS for styling
- Use meaningful component and variable names
- Add JSDoc comments for complex functions

### Backend
- Follow PEP 8 style guide for Python
- Use Django best practices
- Write docstrings for all functions and classes
- Use type hints where appropriate
- Follow REST API conventions

## Commit Messages

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

Example: `feat: add real-time notifications for new messages`

## Testing

- Add tests for new features
- Ensure all existing tests pass
- Test on multiple browsers for frontend changes
- Test API endpoints with different scenarios

## Questions?

Feel free to open an issue for any questions or join our discussions!

## Code of Conduct

Please be respectful and inclusive in all interactions. We're building a welcoming community for everyone.
EOF

    # Security policy
    cat > SECURITY.md << 'EOF'
# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities to **security@evolutionmarket.com**. You will receive a response from us within 48 hours. If the issue is confirmed, we will release a patch as soon as possible depending on complexity but historically within a few days.

**Please do not report security vulnerabilities through public GitHub issues.**

## Security Measures

Evolution Digital Market implements several security measures:

- JWT-based authentication
- Input validation and sanitization
- CORS protection
- Rate limiting
- HTTPS enforcement
- Secure headers
- SQL injection prevention
- XSS protection

## Responsible Disclosure

We kindly ask that you:
- Give us reasonable time to investigate and mitigate an issue before public exposure
- Make a good faith effort to avoid privacy violations and disruptions to others
- Only interact with accounts you own or with explicit permission from the account holder

Thank you for helping keep Evolution Digital Market and our users safe!
EOF

    git add .github/ CONTRIBUTING.md SECURITY.md
    
    print_status "GitHub community files created"
}

# Make scripts executable
make_scripts_executable() {
    print_info "Making deployment scripts executable..."
    
    chmod +x deploy-complete.sh 2>/dev/null || true
    chmod +x deploy-to-railway.sh 2>/dev/null || true
    chmod +x deploy-to-vercel.sh 2>/dev/null || true
    chmod +x deploy-commands.sh 2>/dev/null || true
    
    print_status "Scripts made executable"
}

# Main execution
main() {
    print_header "Evolution Digital Market - GitHub Setup"
    echo "This script will help you push your project to GitHub automatically!"
    echo ""
    
    # Check prerequisites
    check_git
    
    # Check for GitHub CLI
    HAS_GH_CLI=false
    if check_gh_cli; then
        HAS_GH_CLI=true
    fi
    
    # Get repository information
    get_repo_info
    
    # Initialize git
    init_git
    
    # Create project files
    create_gitignore
    create_readme
    create_license
    create_github_files
    make_scripts_executable
    
    # Add files and create commit
    if add_files; then
        create_commit
    else
        print_error "No files to commit. Make sure you have files in your project."
        exit 1
    fi
    
    # Create GitHub repository
    if [ "$HAS_GH_CLI" = true ]; then
        if ! create_repo_with_cli; then
            manual_repo_creation
        fi
    else
        manual_repo_creation
    fi
    
    # Push to GitHub
    if push_to_github; then
        print_status "Project successfully pushed to GitHub! 🎉"
        echo ""
        print_info "Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        echo ""
        
        echo ""
        print_header "🎉 Success!"
        echo "Your Evolution Digital Market is now on GitHub!"
        echo ""
        echo "🔗 Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        echo "📚 Clone URL: $REPO_URL"
        echo ""
        print_info "Next steps:"
        echo "1. Set up deployment: ./deploy-complete.sh"
        echo "2. Configure environment variables"
        echo "3. Invite collaborators"
        echo "4. Set up CI/CD workflows"
        echo "5. Star the repository ⭐"
        echo ""
        print_status "Happy coding! 🚀"
        echo ""
        print_info "Your marketplace is ready to revolutionize P2P trading!"
    else
        print_error "Failed to push to GitHub. Please check your authentication."
        echo ""
        print_info "Manual steps:"
        echo "1. Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        echo "2. Follow the instructions to push an existing repository"
        echo ""
        echo "Or try:"
        echo "git remote add origin $REPO_URL"
        echo "git branch -M main"
        echo "git push -u origin main"
    fi
}

# Run the script
main "$@"