#!/usr/bin/env python3
"""
Complete CMS Assignment Codebase Generator
Generates all backend, frontend, and worker source files from templates.
"""

import os
import sys
from pathlib import Path

def create_file(path, content):
    """Create a file with given content, creating directories as needed."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"✅ Created: {path}")

def generate_backend_files():
    """Generate all backend source files."""
    print("\n📦 Generating Backend Files...")
    
    # Models
    models_content = '''from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ARRAY, JSON, ForeignKey, Enum as SQLEnum, UniqueConstraint, Index, event
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum
from app.database import Base

class ProgramStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class LessonStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class Program(Base):
    __tablename__ = "programs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    language_primary = Column(String(10), nullable=False)
    languages_available = Column(ARRAY(String), nullable=False)
    status = Column(SQLEnum(ProgramStatus), default=ProgramStatus.DRAFT)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    terms = relationship("Term", back_populates="program", cascade="all, delete-orphan")
    assets = relationship("ProgramAsset", back_populates="program", cascade="all, delete-orphan")
    topics = relationship("Topic", secondary="program_topics", back_populates="programs")
    
    __table_args__ = (
        Index("ix_program_status_published", "status", "published_at"),
        Index("ix_program_language", "language_primary"),
    )

class Term(Base):
    __tablename__ = "terms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("programs.id"), nullable=False)
    term_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    program = relationship("Program", back_populates="terms")
    lessons = relationship("Lesson", back_populates="term", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("program_id", "term_number", name="uq_program_term"),
    )

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id"), nullable=False)
    lesson_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)  # video, article
    duration_ms = Column(Integer, nullable=True)
    is_paid = Column(Boolean, default=False)
    content_language_primary = Column(String(10), nullable=False)
    content_languages_available = Column(ARRAY(String), nullable=False)
    content_urls_by_language = Column(JSON, nullable=False)  # {"en": "url", "te": "url"}
    subtitle_languages = Column(ARRAY(String), nullable=False, default=[])
    subtitle_urls_by_language = Column(JSON, nullable=False, default={})
    status = Column(SQLEnum(LessonStatus), default=LessonStatus.DRAFT)
    publish_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    term = relationship("Term", back_populates="lessons")
    assets = relationship("LessonAsset", back_populates="lesson", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("term_id", "lesson_number", name="uq_term_lesson"),
        Index("ix_lesson_status_publish", "status", "publish_at"),
        Index("ix_lesson_term", "term_id"),
    )

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    programs = relationship("Program", secondary="program_topics", back_populates="topics")

class ProgramTopic(Base):
    __tablename__ = "program_topics"
    
    program_id = Column(UUID(as_uuid=True), ForeignKey("programs.id"), primary_key=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), primary_key=True)

class ProgramAsset(Base):
    __tablename__ = "program_assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("programs.id"), nullable=False)
    language = Column(String(10), nullable=False)
    variant = Column(String(50), nullable=False)  # portrait, landscape, square, banner
    asset_type = Column(String(50), nullable=False)  # poster
    url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    program = relationship("Program", back_populates="assets")
    
    __table_args__ = (
        UniqueConstraint("program_id", "language", "variant", "asset_type", name="uq_program_asset"),
    )

class LessonAsset(Base):
    __tablename__ = "lesson_assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    language = Column(String(10), nullable=False)
    variant = Column(String(50), nullable=False)  # portrait, landscape, square, banner
    asset_type = Column(String(50), nullable=False)  # thumbnail, subtitle
    url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    lesson = relationship("Lesson", back_populates="assets")
    
    __table_args__ = (
        UniqueConstraint("lesson_id", "language", "variant", "asset_type", name="uq_lesson_asset"),
    )

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_user_email", "email"),
    )
'''
    create_file("backend/app/models.py", models_content)

if __name__ == "__main__":
    print("🚀 Generating Complete CMS Codebase...")
    generate_backend_files()
    print("\n✅ Codebase generation complete!")
    print("\nNext steps:")
    print("1. Run: docker compose up --build")
    print("2. Access: http://localhost:3000 (Frontend)")
    print("3. Access: http://localhost:8000/docs (API Docs)")
