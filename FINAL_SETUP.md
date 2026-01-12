FINAL_SETUP.sh# CMS Assignment - Final Setup & Deployment Guide

## Project Structure Complete

This project contains a complete CMS (Content Management System) built with:
- **Backend**: FastAPI with SQLAlchemy ORM
- **Frontend**: React
- **Worker**: Scheduled publishing task
- **Database**: PostgreSQL
- **Deployment**: Docker & Docker Compose

## Files Created

### Backend (`/backend`)
- `app/main.py` - FastAPI application entry point
- `app/models.py` - Database models with constraints
- `app/schemas.py` - Pydantic schemas for validation
- `app/database.py` - Database connection setup  
- `app/config.py` - Configuration management
- `app/auth.py` - JWT authentication
- `app/routers/` - API endpoints
  - `auth.py` - Login/authentication endpoints
  - `programs.py` - Program CRUD endpoints
  - `lessons.py` - Lesson CRUD endpoints
  - `assets.py` - Asset upload/download endpoints
- `worker.py` - Scheduled publishing worker (60-second intervals)
- `requirements.txt` - Python dependencies
- `Dockerfile` - Backend container image

### Frontend (`/frontend`)
- `package.json` - React dependencies
- `public/index.html` - HTML entry point
- `src/index.js` - React initialization
- `src/App.js` - Main React component
- `src/components/` - Reusable UI components
- `Dockerfile` - Frontend container image

### Configuration
- `docker-compose.yml` - Multi-container orchestration
- `.gitignore` - Git ignore patterns

## Local Development Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Docker & Docker Compose

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Run with Docker Compose
```bash
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Programs
- `GET /programs/` - List all programs
- `POST /programs/` - Create program (admin/editor only)
- `GET /programs/{id}` - Get program details
- `PUT /programs/{id}` - Update program
- `DELETE /programs/{id}` - Delete program

### Lessons
- `GET /lessons/` - List lessons
- `POST /lessons/` - Create lesson
- `PUT /lessons/{id}` - Update lesson
- `DELETE /lessons/{id}` - Delete lesson
- `POST /lessons/{id}/publish` - Publish lesson
- `POST /lessons/{id}/schedule` - Schedule lesson publishing

### Assets
- `POST /assets/upload` - Upload asset file
- `GET /assets/` - List assets
- `DELETE /assets/{id}` - Delete asset

## Worker (Background Job)

The worker runs every 60 seconds and:
1. Queries for lessons with status='scheduled'
2. Checks if scheduled_publish_time <= current_time
3. Updates status to 'published'
4. Logs the action in PublishingLog table
5. Ensures idempotent operation

## Database Schema

### Users Table
- id (PK)
- username (unique)
- email (unique)
- hashed_password
- role (admin/editor/viewer)
- created_at
- updated_at

### Programs Table
- id (PK)
- name (unique)
- description
- created_by (FK -> Users)
- created_at
- updated_at

### Lessons Table
- id (PK)
- program_id (FK)
- title
- content
- status (draft/scheduled/published)
- scheduled_publish_time
- published_at
- created_by (FK -> Users)
- created_at
- updated_at

### Assets Table
- id (PK)
- filename
- file_path
- program_id (FK, nullable)
- lesson_id (FK, nullable)
- uploaded_by (FK -> Users)
- created_at

### PublishingLog Table
- id (PK)
- lesson_id (FK)
- action
- timestamp
- status
- details

## Constraints & Indexes

- Unique constraints on (username, email, program name)
- Foreign key constraints with CASCADE delete
- Indexes on frequently queried fields (status, user_id, program_id)
- Timestamps (created_at, updated_at) on all tables
- Worker idempotency: Only processes lessons not already published

## Deployment

### Via Docker Compose (Local)
```bash
docker-compose up --build
```

### Via Railway
1. Connect GitHub repository to Railway
2. Create PostgreSQL database service
3. Deploy backend service pointing to `/backend`
4. Deploy frontend service pointing to `/frontend`
5. Configure environment variables

## Environment Variables

Create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/cms_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REACT_APP_API_URL=http://localhost:8000
```

## Testing the Assignment

1. Start all services with Docker Compose
2. Access frontend at `http://localhost:3000`
3. Login with test credentials
4. Create programs and lessons
5. Schedule lessons for publishing
6. Observe worker publishing them automatically
7. Check publishing logs

## Submission Checklist

- [x] GitHub repo created
- [x] Backend API with all endpoints
- [x] React CMS UI
- [x] Worker with 60-second scheduling
- [x] Database constraints and indexes
- [x] Docker setup
- [x] Deployment-ready
- [x] Complete README
- [x] All requirements met

## Additional Notes

- All endpoints require proper authentication except login
- Role-based access control implemented
- Lessons can be drafted, scheduled, or published
- Worker ensures publishing happens exactly once
- All timestamps use UTC
- API follows RESTful conventions
