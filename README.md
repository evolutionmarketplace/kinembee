# 🚀 Evolution Digital Market

A modern, full-stack peer-to-peer marketplace with completely separated frontend and backend for easier deployment and development.

![Evolution Market](https://images.pexels.com/photos/230544/pexels-photo-230544.jpeg?auto=compress&cs=tinysrgb&w=1200)

## 📁 Project Structure

```
evolution-digital-market/
├── frontend/                 # React Frontend Application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/         # React context providers
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API services
│   │   ├── types/           # TypeScript definitions
│   │   ├── utils/           # Utility functions
│   │   ├── config/          # Configuration files
│   │   └── data/            # Mock data
│   ├── public/              # Static assets
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.ts       # Vite configuration
│   └── vercel.json          # Vercel deployment config
│
├── backend/                  # Django Backend Application
│   ├── apps/                # Django applications
│   │   ├── accounts/        # User management
│   │   ├── products/        # Product listings
│   │   ├── categories/      # Product categories
│   │   ├── reviews/         # Review system
│   │   ├── chat/            # Real-time messaging
│   │   ├── payments/        # Payment processing
│   │   └── notifications/   # Notification system
│   ├── evolution_market/    # Django project settings
│   ├── requirements.txt     # Python dependencies
│   ├── manage.py           # Django management
│   └── railway.json        # Railway deployment config
│
└── docs/                    # Documentation
```

## 🎯 Quick Start

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🚀 Deployment

### Frontend (Vercel)
1. Connect your GitHub repo to Vercel
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_URL=https://your-backend.railway.app`
4. Deploy automatically on push

### Backend (Railway)
1. Connect your GitHub repo to Railway
2. Set root directory to `backend`
3. Add environment variables (see backend/.env.example)
4. Deploy automatically on push

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

## 🔧 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
RESEND_API_KEY=your-resend-api-key
STRIPE_SECRET_KEY=sk_test_your-stripe-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
```

## 🌐 Free Deployment

Deploy your entire marketplace for **$0/month** using our free tier setup:

**Free Services Used:**
- **Vercel** - Frontend hosting (Free)
- **Railway** - Backend hosting ($5 free credit/month)
- **Supabase** - PostgreSQL database (Free tier)
- **Cloudinary** - Image storage (Free tier)
- **Resend** - Email service (3,000 emails/month free)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📊 API Documentation

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
- **SQL Injection Protection** - Django ORM safety

## 📈 Performance

- **Optimized Images** - Automatic compression and WebP conversion
- **Lazy Loading** - Images and components load on demand
- **Code Splitting** - Reduced bundle sizes
- **Caching** - Redis-powered caching layer
- **CDN** - Global content delivery
- **Database Optimization** - Indexed queries and connection pooling

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **React Team** - For the amazing React library
- **Django Team** - For the robust Django framework
- **Tailwind CSS** - For the utility-first CSS framework
- **Stripe** - For secure payment processing
- **Vercel** - For excellent hosting platform

## 📞 Support

- **Documentation**: [docs.evolutionmarket.com](https://docs.evolutionmarket.com)
- **Community**: [Discord](https://discord.gg/evolutionmarket)
- **Email**: support@evolutionmarket.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/evolution-digital-market/issues)

---

**Built with ❤️ by the Evolution Market Team**

[🌟 Star us on GitHub](https://github.com/yourusername/evolution-digital-market) | [🐦 Follow on Twitter](https://twitter.com/evolutionmarket) | [💼 LinkedIn](https://linkedin.com/company/evolutionmarket)