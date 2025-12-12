# Quick Start Guide

## Getting Started in 5 Minutes

### Prerequisites Check
```bash
# Verify Docker is installed
docker --version
docker-compose --version

# Expected output: Docker version 20.10+ and docker-compose version 1.29+
```

### 1. Clone and Setup (1 minute)

```bash
# Clone repository
git clone https://github.com/lankamar/nurse-eval-ai.git
cd nurse-eval-ai

# Copy environment file
cp .env.example .env
```

### 2. Start the Application (2 minutes)

```bash
# Start all services
docker-compose up -d

# Wait for services to be ready (watch logs)
docker-compose logs -f

# You should see:
# - PostgreSQL ready to accept connections
# - Backend: Application startup complete
# - Frontend: webpack compiled successfully
```

### 3. Initialize Database (1 minute)

```bash
# Seed database with initial data
docker-compose exec backend python -m app.db.seed

# Expected output:
# Successfully seeded 25 evaluation criteria (11 technical + 14 attitudinal)
# Created admin user (username: admin, password: admin123)
```

### 4. Access the Application (1 minute)

Open your browser and navigate to:

**Frontend**: http://localhost:3000
**API Documentation**: http://localhost:8000/docs
**Backend API**: http://localhost:8000

### 5. Login and Test

1. Go to http://localhost:3000
2. Click "Iniciar Sesión"
3. Use these credentials:
   - Username: `admin`
   - Password: `admin123`
4. You're in! 🎉

## What's Next?

### Create Your First User
1. Register a new user with the Enfermero role
2. Login as admin
3. View the user in the system

### Create Your First Evaluation
1. Login as admin or create a Supervisora user
2. Go to Dashboard
3. Click "Nueva Evaluación"
4. Select a user to evaluate
5. Start the chatbot conversation

### Generate Your First PDF
1. Complete an evaluation (all 25 criteria)
2. Click "Complete Evaluation"
3. Generate PDF report
4. Download and review the auditable PDF

## Common Issues

### Port Already in Use
```bash
# Stop conflicting services
docker-compose down
sudo lsof -i :3000  # Check what's using the port
sudo lsof -i :8000
sudo lsof -i :5432
```

### Database Connection Failed
```bash
# Reset database
docker-compose down -v
docker-compose up -d
docker-compose exec backend python -m app.db.seed
```

### Frontend Won't Start
```bash
# Rebuild frontend
docker-compose down
docker-compose build frontend
docker-compose up -d frontend
```

### Permission Denied
```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
# Logout and login again
```

## Development Mode

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Run Tests
```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

## API Quick Reference

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","full_name":"Test User","password":"test123456","role":"enfermero"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

## Production Deployment

For production deployment, see [DEPLOYMENT.md](docs/DEPLOYMENT.md)

Key steps:
1. Configure production environment variables
2. Set up SSL/TLS certificates
3. Use managed PostgreSQL database
4. Configure Sentry for monitoring
5. Set up backups
6. Configure firewall rules

## Need Help?

- 📖 Full Documentation: [README.md](README.md)
- 🚀 API Examples: [docs/API_EXAMPLES.md](docs/API_EXAMPLES.md)
- 🔒 Compliance: [docs/COMPLIANCE.md](docs/COMPLIANCE.md)
- 🤝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- 🐛 Report Issues: GitHub Issues

## Video Tutorial

Coming soon: Step-by-step video walkthrough of the system.

## Summary

You now have a fully functional nurse evaluation system with:
- ✅ FastAPI backend with JWT + 2FA authentication
- ✅ React responsive frontend
- ✅ PostgreSQL database with 25 evaluation criteria
- ✅ Conversational chatbot for evaluations
- ✅ Automatic score calculation
- ✅ PDF generation with audit trail
- ✅ RBAC with 4 role levels
- ✅ Full compliance with Decreto 366/06, Ley 25.326, and RENFAMED

Enjoy using Nurse Eval AI! 🏥⚕️
