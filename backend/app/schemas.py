from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class ProgramStatusEnum(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class LessonStatusEnum(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict

class ProgramCreate(BaseModel):
    title: str
    description: Optional[str] = None
    language_primary: str
    languages_available: List[str]

class LessonCreate(BaseModel):
    term_id: str
    lesson_number: int
    title: str
    content_type: str
    duration_ms: Optional[int] = None
    is_paid: bool = False
    content_language_primary: str
    content_languages_available: List[str]
    content_urls_by_language: Dict[str, str]

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[LessonStatusEnum] = None
    publish_at: Optional[datetime] = None

class ProgramResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    language_primary: str
    languages_available: List[str]
    status: ProgramStatusEnum
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
