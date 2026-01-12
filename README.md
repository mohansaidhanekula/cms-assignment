# CMS Assignment - Complete Implementation

## 🎯 Project Overview

A complete **Content Management System (CMS)** built with FastAPI, React, PostgreSQL, and Docker. This project demonstrates a production-ready application with role-based access control, scheduled publishing, and comprehensive API endpoints.

**Repository**: https://github.com/mohansaidhanekula/cms-assignment

## 📋 Project Structure

```
cms-assignment/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── database.py          # Database setup
│   │   ├── config.py            # Configuration
│   │   ├── auth.py              # JWT authentication
│   │   ├── worker.py            # Background worker
│   │   └── routers/             # API endpoints
│   │       ├── auth.py          # Authentication routes
│   │       ├── programs.py      # Program CRUD
│   │       ├── lessons.py       # Lesson CRUD & Publishing
│   │       └── assets.py        # Asset management
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── index.js
│   │   ├── App.js
│   │   └── components/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── README.md
└── FINAL_SETUP.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/mohansaidhanekula/cms-assignment.git
cd cms-assignment

# 2. Start all services
docker-compose up --build

# Services will be available at:
# Backend API: http://localhost:8000
# Frontend UI: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Database: postgresql://localhost:5432/cms_db
```

## 🔐 Authentication

The system uses JWT token-based authentication with three roles:
- **Admin**: Full access to all resources
- **Editor**: Can create and edit content
- **Viewer**: Read-only access

### Login Endpoint
```bash
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```

## 📡 API Endpoints

### Programs
- `GET /programs/` - List all programs
- `POST /programs/` - Create program
- `GET /programs/{id}` - Get program details
- `PUT /programs/{id}` - Update program
- `DELETE /programs/{id}` - Delete program

### Lessons
- `GET /lessons/` - List lessons
- `POST /lessons/` - Create lesson
- `GET /lessons/{id}` - Get lesson details
- `PUT /lessons/{id}` - Update lesson
- `DELETE /lessons/{id}` - Delete lesson
- `POST /lessons/{id}/publish` - Publish immediately
- `POST /lessons/{id}/schedule` - Schedule for publishing

### Assets
- `POST /assets/upload` - Upload asset file
- `GET /assets/` - List assets with filters
- `DELETE /assets/{id}` - Delete asset

## ⏰ Background Worker

A scheduled worker runs every **60 seconds** and:
1. Queries for lessons with `status='scheduled'`
2. Checks if `scheduled_publish_time <= current_time`
3. Updates lesson status to `published`
4. Logs publishing action in PublishingLog table
5. Ensures idempotent operation (no duplicates)

## 📊 Database Schema

### Key Tables
- **Users**: User accounts with roles
- **Programs**: Content programs/courses
- **Lessons**: Individual lessons within programs
- **Assets**: Uploaded files and media
- **PublishingLog**: Audit trail of publishing events

### Constraints & Indexes
- Unique constraints on username, email, program names
- Foreign key constraints with CASCADE delete
- Indexes on frequently queried fields
- Proper timestamps (created_at, updated_at) on all tables

## 🛠 Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database
- Pydantic - Data validation
- JWT - Secure authentication
- asyncio - Async tasks

**Frontend:**
- React 18 - UI library
- Axios - HTTP client
- React Router - Client-side routing

**Infrastructure:**
- Docker - Containerization
- Docker Compose - Multi-container orchestration
- PostgreSQL - Relational database

## 📋 Implementation Checklist

- [x] GitHub repository created
- [x] Complete backend API implementation
- [x] React frontend UI/CMS
- [x] Worker with 60-second scheduling
- [x] Database models with constraints
- [x] Role-based access control
- [x] JWT authentication
- [x] Asset management
- [x] Publishing workflow
- [x] Docker & Docker Compose setup
- [x] Comprehensive documentation
- [x] Deployment-ready configuration

## 📚 Documentation

For detailed setup and deployment instructions, see **[FINAL_SETUP.md](FINAL_SETUP.md)**

For assignment specifications, see **[ASSIGNMENT_SUBMISSION.md](ASSIGNMENT_SUBMISSION.md)**

## 🚢 Deployment

### Docker Compose (Recommended for local/testing)
```bash
docker-compose up --build
```

### Railway Deployment
1. Connect GitHub repository to Railway
2. Create PostgreSQL service
3. Deploy backend service (pointing to `/backend` directory)
4. Deploy frontend service (pointing to `/frontend` directory)
5. Configure environment variables:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-secret-key
   REACT_APP_API_URL=https://your-backend-url.railway.app
   ```

## 📧 Contact

**Author**: mohansaidhanekula  
**Repository**: https://github.com/mohansaidhanekula/cms-assignment

## 📄 License

This project is created as a take-home assignment for demonstration purposes.

---

**Status**: ✅ Complete and ready for submission
