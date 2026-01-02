# 🐌 Snail Mail Dashboard

Transform your email analytics into a delightful snail race! **Snail Mail Dashboard** is a full-stack web application that visualizes your Gmail activity as animated snails racing across your screen. Each snail represents different email categories, with their speed and appearance reflecting your email volume, response times, and activity patterns.
<!-- 
## Features

- **Animated Snail Race Visualization**: Watch snails race across your dashboard, each representing different email categories (work, personal, promotions)
- **Historical Timeline**: Browse through your email activity history with an interactive carousel
- **Real-time Analytics**: Track inbox volume, sent messages, response times, and category distributions
- **Google OAuth Integration**: Securely connect your Gmail account
- **Gmail API Integration**: Automatically sync and analyze your email metadata
- **Background Processing**: Efficient email syncing and analytics computation via Celery
- **Interactive Charts**: Visualize trends with beautiful, responsive charts
- **Daily/Weekly Reports**: Get insights into your email habits -->

## Tech Stack

### Backend
- **Django 5.2.8** - Python web framework
- **PostgreSQL 16** - Relational database
- **Celery 5.5.3** - Distributed task queue
- **Redis 7** - Message broker and cache
- **Django REST Framework 3.16** - API layer
- **Google APIs** - Gmail integration
- **Django Allauth** - Authentication with OAuth2

### Frontend
- **Next.js 16** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **Radix UI** - Accessible component primitives
- **Recharts** - Data visualization
- **Embla Carousel** - Timeline carousel

## Prerequisites

- **Python 3.11+** (recommend using a virtual environment)
- **Node.js 18+** and npm
- **Docker & Docker Compose** (for PostgreSQL and Redis)
- **Google Cloud Project** with Gmail API enabled
- **Gmail account** for testing

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd snailmail
```

### 2. Start Docker Services

```bash
docker-compose up -d
```

This starts PostgreSQL (port 5433) and Redis (port 6379).

### 3. Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
```

Django will be available at `http://localhost:8000`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start Next.js development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 5. Configure Google OAuth

1. **Access Django Admin**
   - Navigate to `http://localhost:8000/admin/`
   - Log in with your superuser credentials

2. **Add Google Social Application**
   - Click on **Social applications** under **Social accounts**
   - Click **Add social application**
   - Fill in the following:
     - **Provider**: Select `Google`
     - **Name**: `Google` (or any name you prefer)
     - **Client id**: Your Google OAuth Client ID from `.env`
     - **Secret key**: Your Google OAuth Client Secret from `.env`
     - **Sites**: Select `example.com` and move it to "Chosen sites"
   - Click **Save**

3. **Verify Configuration**
   - Visit `http://localhost:8000/api/auth/google/login/`
   - You should be redirected to Google's OAuth consent screen

Your Google OAuth is now configured and ready to use!

## Project Structure

```
snailmail/
├── authentication/          # User authentication & OAuth
│   ├── models.py           # User models
│   ├── views.py            # Auth endpoints (CSRF, auth status)
│   └── urls.py
├── mail/                   # Email data management
│   ├── models.py           # Message, GmailSyncState models
│   ├── tasks.py            # Celery tasks for email sync
│   ├── views.py            # Email API endpoints
│   └── admin.py            # Django admin configuration
├── analytics/              # Email analytics computation
│   ├── models.py           # DailyStat model
│   ├── tasks.py            # Analytics aggregation tasks
│   └── views.py            # Analytics API endpoints
├── snailmail/              # Django project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # URL routing
│   └── celery.py           # Celery configuration
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/    # React components
│   │   │   ├── snail.tsx          # Main snail race
│   │   │   ├── analytics-dialog.tsx
│   │   │   └── ui/                # Radix UI components
│   │   ├── hooks/         # Custom React hooks
│   │   └── lib/           # Utilities
│   └── package.json
├── docker-compose.yml      # PostgreSQL + Redis services
├── requirements.txt        # Python dependencies
└── development_guide.md  # Detailed setup instructions
```

Built with ❤️ as a playful take on email analytics.