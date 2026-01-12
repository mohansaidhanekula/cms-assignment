from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ..models import Asset, Program, Lesson
from ..schemas import AssetCreate, AssetResponse
from ..database import get_db
from ..auth import get_current_user
import shutil
import os
from pathlib import Path

router = APIRouter(prefix="/assets", tags=["assets"])

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload", response_model=AssetResponse)
async def upload_asset(
    file: UploadFile = File(...),
    program_id: int = None,
    lesson_id: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Upload an asset file"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    asset = Asset(
        filename=file.filename,
        file_path=str(file_path),
        program_id=program_id,
        lesson_id=lesson_id,
        uploaded_by=current_user.id
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@router.get("/", response_model=List[AssetResponse])
def list_assets(
    program_id: int = None,
    lesson_id: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List assets"""
    query = db.query(Asset)
    if program_id:
        query = query.filter(Asset.program_id == program_id)
    if lesson_id:
        query = query.filter(Asset.lesson_id == lesson_id)
    return query.all()

@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete an asset"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    try:
        os.remove(asset.file_path)
    except:
        pass
    
    db.delete(asset)
    db.commit()
    return {"message": "Asset deleted"}
