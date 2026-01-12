from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ARRAY, JSON, ForeignKey, Enum as SQLEnum, UniqueConstraint, Index
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
    __table_args__ = (Index("ix_program_status", "status"),)

class Term(Base):
    __tablename__ = "terms"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("programs.id"), nullable=False)
    term_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    program = relationship("Program", back_populates="terms")
    lessons = relationship("Lesson", back_populates="term", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("program_id", "term_number", name="uq_program_term"),)

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id"), nullable=False)
    lesson_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)
    duration_ms = Column(Integer, nullable=True)
    is_paid = Column(Boolean, default=False)
    content_language_primary = Column(String(10), nullable=False)
    content_languages_available = Column(ARRAY(String), nullable=False)
    content_urls_by_language = Column(JSON, nullable=False)
    subtitle_languages = Column(ARRAY(String), nullable=False, default=[])
    subtitle_urls_by_language = Column(JSON, nullable=False, default={})
    status = Column(SQLEnum(LessonStatus), default=LessonStatus.DRAFT)
    publish_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    term = relationship("Term", back_populates="lessons")
    assets = relationship("LessonAsset", back_populates="lesson", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("term_id", "lesson_number", name="uq_term_lesson"), Index("ix_lesson_status_publish", "status", "publish_at"))

class Topic(Base):
    __tablename__ = "topics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProgramAsset(Base):
    __tablename__ = "program_assets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("programs.id"), nullable=False)
    language = Column(String(10), nullable=False)
    variant = Column(String(50), nullable=False)
    asset_type = Column(String(50), nullable=False)
    url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    program = relationship("Program", back_populates="assets")
    __table_args__ = (UniqueConstraint("program_id", "language", "variant", "asset_type", name="uq_program_asset"),)

class LessonAsset(Base):
    __tablename__ = "lesson_assets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    language = Column(String(10), nullable=False)
    variant = Column(String(50), nullable=False)
    asset_type = Column(String(50), nullable=False)
    url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    lesson = relationship("Lesson", back_populates="assets")
    __table_args__ = (UniqueConstraint("lesson_id", "language", "variant", "asset_type", name="uq_lesson_asset"),)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (Index("ix_user_email", "email"),)
