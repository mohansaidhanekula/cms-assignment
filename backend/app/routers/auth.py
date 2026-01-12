auth.py  from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LoginRequest, TokenResponse, UserResponse
from app.auth import create_access_token, get_password_hash, verify_password, seed_users_dict
from app.models import User, UserRole
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Demo users dictionary
DEMO_USERS = seed_users_dict()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint with JWT token generation"""
    
    # First try database
    user = db.query(User).filter(User.email == request.email).first()
    
    if user is None:
        # Try demo users
        if request.email in DEMO_USERS:
            demo_user = DEMO_USERS[request.email]
            if verify_password(request.password, demo_user["password_hash"]):
                # Create JWT token
                access_token_expires = timedelta(minutes=30)
                access_token = create_access_token(
                    data={"sub": request.email, "role": demo_user["role"]},
                    expires_delta=access_token_expires
                )
                return TokenResponse(
                    access_token=access_token,
                    user={
                        "email": request.email,
                        "role": demo_user["role"],
                        "is_active": demo_user["is_active"]
                    }
                )
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        user={
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "is_active": user.is_active
        }
    )

@router.get("/me", response_model=UserResponse)
def get_current_user(db: Session = Depends(get_db), token: str = None):
    """Get current user from token"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = db.query(User).filter(User.email == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
