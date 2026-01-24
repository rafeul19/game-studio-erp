# 🎮 Game Studio ERP System - Setup Guide

## 📋 Prerequisites

- Python 3.10+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional but recommended)

---

## 🚀 Quick Start with Docker (Recommended)

### 1. Clone and Setup Environment

```bash
# Clone the repository
cd /home/abcd/projects/erp-system

# Create backend environment file
cp backend/.env.example backend/.env

# Edit backend/.env and update values
nano backend/.env
```

### 2. Start All Services

```bash
# Build and start all containers
docker-compose up --build

# The services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

### 3. Initialize Database

```bash
# Run migrations (in a new terminal)
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend Admin**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/

---

## 🔧 Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and configure database
nano .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Start Celery Worker (Separate Terminal)

```bash
cd backend
source venv/bin/activate
celery -A backend worker -l info
```

### Start Celery Beat (Separate Terminal)

```bash
cd backend
source venv/bin/activate
celery -A backend beat -l info
```

---

## 🗄️ Database Configuration

### PostgreSQL Setup

```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

CREATE DATABASE erp_gamedev;
CREATE USER erp_user WITH PASSWORD 'your_secure_password';
ALTER ROLE erp_user SET client_encoding TO 'utf8';
ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE erp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE erp_gamedev TO erp_user;
\q
```

### Update backend/.env

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_gamedev
DB_USER=erp_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 🔴 Redis Setup

```bash
# Install Redis
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis
redis-cli ping
# Should return: PONG
```

---

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest erp_projects/tests/test_models.py
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

---

## 📦 Building for Production

### Backend

```bash
cd backend

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
pip install gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

### Frontend

```bash
cd frontend

# Build production bundle
npm run build

# Start production server
npm start
```

---

## 🐳 Docker Commands

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Rebuild containers
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access backend shell
docker-compose exec backend python manage.py shell

# Access PostgreSQL
docker-compose exec db psql -U erp_user -d erp_gamedev

# Access Redis CLI
docker-compose exec redis redis-cli
```

---

## 🔒 Environment Variables

### Backend (.env)

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_gamedev
DB_USER=erp_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password

# AWS S3 (optional)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🛠️ Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Error

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U erp_user -d erp_gamedev -h localhost
```

### Redis Connection Error

```bash
# Check Redis is running
sudo systemctl status redis-server

# Test connection
redis-cli ping
```

### Docker Issues

```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose up --build --force-recreate
```

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Django Channels Documentation](https://channels.readthedocs.io/)

---

## 🎯 Next Steps

1. ✅ Complete Phase 1 infrastructure setup
2. ✅ Run migrations and create superuser
3. ✅ Test WebSocket connections
4. ✅ Implement file upload functionality
5. ✅ Build HR and Finance modules
6. ✅ Add comprehensive testing
7. ✅ Set up CI/CD pipeline

---

**Happy Coding! 🚀**
