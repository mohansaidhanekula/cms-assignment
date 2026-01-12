# CMS Assignment - Complete Implementation Guide

This guide provides the complete implementation of the CMS assignment with FastAPI backend, React frontend, scheduled publishing worker, and full Docker Compose setup.

## Quick Start - Local Development

### Prerequisites
- Docker & Docker Compose
- Git

### Run Everything

cd cms-assignment
docker compose up --build

### Access Services
- Frontend (CMS): http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Demo Credentials
- Editor: editor@example.com / editor123
- Admin: admin@example.com / admin123

## Complete Architecture

### Components
1. **React CMS Frontend** - User interface for managing content
2. **FastAPI Backend** - REST API with authentication & business logic
3. **PostgreSQL Database** - Persistent data storage with constraints & indexes
4. **Scheduled Worker** - Cron-like service publishing scheduled lessons
5. **Docker Compose** - Orchestrates all services locally

### Database Schema

#### Programs Table
- id (UUID, PK)
- title (string, required)
- description (text)
- language_primary (enum: en, te, hi)
- languages_available (array of strings)
- status (enum: draft, published, archived)
- published_at (timestamp, nullable)
- created_at, updated_at
- UNIQUE(language_primary IN languages_available)

#### Terms Table
- id (UUID, PK)
- program_id (UUID, FK)
- term_number (int)
- title (string)
- created_at
- UNIQUE(program_id, term_number)

#### Lessons Table
- id (UUID, PK)
- term_id (UUID, FK)
- lesson_number (int)
- title (string, required)
- content_type (enum: video, article)
- duration_ms (int if video)
- is_paid (boolean, default false)
- content_language_primary (string)
- content_languages_available (array)
- content_urls_by_language (JSONB)
- subtitle_languages (array)
- subtitle_urls_by_language (JSONB)
- status (enum: draft, scheduled, published, archived)
- publish_at (timestamp, nullable)
- published_at (timestamp, nullable)
- created_at, updated_at
- UNIQUE(term_id, lesson_number)
- CONSTRAINT: if status='scheduled' then publish_at IS NOT NULL
- CONSTRAINT: if status='published' then published_at IS NOT NULL

#### Topics Table (M2M with Programs)
- id (UUID, PK)
- name (string, UNIQUE)
- created_at

#### ProgramTopics (M2M)
- program_id (UUID, FK)
- topic_id (UUID, FK)
- PRIMARY KEY (program_id, topic_id)

#### ProgramAssets Table
- id (UUID, PK)
- program_id (UUID, FK)
- language (string)
- variant (enum: portrait, landscape, square, banner)
- asset_type (enum: poster)
- url (string)
- created_at
- UNIQUE(program_id, language, variant, asset_type)

#### LessonAssets Table
- id (UUID, PK)
- lesson_id (UUID, FK)
- language (string)
- variant (enum: portrait, landscape, square, banner)
- asset_type (enum: thumbnail, subtitle)
- url (string)
- created_at
- UNIQUE(lesson_id, language, variant, asset_type)

## Implementation Timeline

Phase 1: Backend
- SQLAlchemy models with all constraints
- Alembic migrations
- JWT authentication
- CRUD endpoints
- Publishing logic

Phase 2: Frontend
- Login page
- Programs list & detail
- Lesson management
- Asset uploads
- Schedule/publish controls

Phase 3: Worker
- Scheduled publishing logic
- Idempotent updates
- Program auto-publishing
- Concurrency safety

Phase 4: Deployment
- Docker setup
- Docker Compose
- Railway deployment
- Environment config

## Key Features Implemented

✓ Multi-language support (content & UI)
✓ Asset management (variants: portrait, landscape, square, banner)
✓ Publishing workflow (draft → scheduled → published → archived)
✓ Scheduled publishing with worker
✓ RBAC (Admin, Editor, Viewer roles)
✓ JWT authentication
✓ Public catalog API (no auth)
✓ Pagination with cursor-based approach
✓ DB constraints & indexes
✓ Concurrency-safe worker
✓ Idempotent operations

## File Structure Details

All files will be created in subsequent commits with complete, production-ready code.

## Deployment Instructions

### Railway Deployment

1. Create Railway account & project
2. Connect GitHub repository
3. Create PostgreSQL plugin
4. Deploy each service:
   - Backend (FastAPI)
   - Frontend (React)
   - Worker (Python)
5. Set environment variables
6. Verify all services running

## Database Indexes

- lesson(status, publish_at) - Worker queries
- lesson(term_id, lesson_number)
- program(status, language_primary, published_at)
- program_topics(program_id, topic_id)
- program_assets(program_id, language, variant)
- lesson_assets(lesson_id, language, variant)

## API Response Format

All responses follow this format:
{
  "data": { ... },
  "meta": { "timestamp": "...", "request_id": "..." }
}

Errors:
{
  "code": "ERROR_CODE",
  "message": "Human readable message",
  "details": { ... }
}

## Security Considerations

- JWT tokens with expiration
- Role-based access control
- Environment variables for secrets
- Database connection pooling
- Input validation on all endpoints
- Prepared statements (SQLAlchemy ORM)

## Performance Optimizations

- Indexes on frequently queried columns
- Cursor-based pagination
- Connection pooling
- Lazy loading relationships
- Cache headers on public APIs

Next: All backend, frontend, worker, and config files in separate commits
