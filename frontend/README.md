# 🎨 Evolution Digital Market - Frontend

Modern React frontend for the Evolution Digital Market P2P marketplace platform.

## 🚀 Tech Stack

- **React 18** - Modern UI library with hooks
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vite** - Lightning-fast build tool
- **Lucide React** - Beautiful icons

## 🛠️ Development

### Prerequisites
- Node.js 18+
- npm

### Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables
Create a `.env` file:
```env
VITE_API_URL=http://localhost:8000
```

For production:
```env
VITE_API_URL=https://your-backend.railway.app
```

## 📦 Deployment

### Vercel (Recommended)
```bash
npm run deploy:vercel
```

Or connect your GitHub repo to Vercel for automatic deployments.

### Netlify
```bash
npm run deploy:netlify
```

### GitHub Pages
```bash
npm run deploy
```

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   ├── context/            # React context providers
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API services
│   ├── types/              # TypeScript type definitions
│   ├── utils/              # Utility functions
│   ├── config/             # Configuration files
│   └── data/               # Mock data and constants
├── public/                 # Static assets
├── dist/                   # Build output
└── ...config files
```

## 🎨 Features

- **Responsive Design** - Mobile-first approach
- **Real-time Updates** - Live notifications and chat
- **Advanced Search** - Powerful filtering and search
- **User Authentication** - Secure login/registration
- **Product Management** - Create, edit, and manage listings
- **Chat System** - Real-time messaging between users
- **Payment Integration** - Stripe payment processing
- **Progressive Web App** - App-like experience

## 🔧 Configuration

### API Integration
The frontend connects to the Django backend via REST API. Configure the backend URL in environment variables.

### Authentication
Uses JWT tokens for secure authentication with automatic token refresh.

### State Management
Uses React Context API for global state management.

## 📱 Mobile Support

Fully responsive design with PWA capabilities for mobile app-like experience.

## 🚀 Performance

- Code splitting for optimal loading
- Image optimization and lazy loading
- Efficient bundle sizes with Vite
- Caching strategies for better performance

## 🔒 Security

- XSS protection
- CSRF protection
- Secure API communication
- Input validation and sanitization

Built with ❤️ for the Evolution Digital Market