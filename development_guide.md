## Development Workflow

### Backend Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Django server
python manage.py runserver

# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Django shell
python manage.py shell

# Access admin panel
# http://localhost:8000/admin/
```

### Frontend Commands

```bash
cd frontend

# Development server
npm run dev

# Production build
npm run build

# Production server
npm start

# Lint code
npm run lint
```

### Background Jobs (Celery)

```bash
# Start Celery worker
celery -A snailmail worker -l info

# Test a task
python manage.py shell
>>> from mail.tasks import ping
>>> ping.delay()
```

### Docker Services

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f db
docker-compose logs -f redis

# Check status
docker-compose ps
```

## Setup Google Oath 
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


## 🔌 API Endpoints

### Authentication
- `GET /api/auth/csrf/` - Get CSRF token
- `GET /api/auth/status/` - Check authentication status
- `GET /accounts/google/login/` - Initiate Google OAuth
- `GET /accounts/logout/` - Logout

### Analytics
- `GET /api/analytics/daily-stats/` - Get daily email statistics
- `GET /api/analytics/summary/` - Get aggregated summary

### Email Management
- `GET /api/messages/` - List user's email messages
- `POST /admin/mail/gmailsyncstate/` - Trigger Gmail sync (admin action)

## Testing

### Quick Test Checklist

1. **Backend Authentication**
   ```bash
   curl http://localhost:8000/api/auth/status/
   ```

2. **Database Connection**
   ```bash
   python manage.py dbshell
   ```

3. **Frontend Rendering**
   - Visit `http://localhost:3000`
   - Check browser console for errors

4. **End-to-End OAuth Flow**
   - Login with Google
   - Verify session persists
   - Check API calls succeed

## Environment Variables

Key environment variables (with defaults):

```bash
# Database
POSTGRES_DB=snailmail
POSTGRES_USER=snailmail
POSTGRES_PASSWORD=snailmail
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

# Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Django
SECRET_KEY=<your-secret-key>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Storage (optional)
STORAGE_BACKEND=local  # or 'minio'
AWS_ACCESS_KEY_ID=<minio-key>
AWS_SECRET_ACCESS_KEY=<minio-secret>
```