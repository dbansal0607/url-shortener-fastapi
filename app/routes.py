from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas
from .base62 import encode
import os
router = APIRouter()


BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/shorten", response_model=schemas.URLResponse)
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):

    # Insert first to get ID
    db_url = models.URL(original_url=url.original_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    # Generate short code from ID
    short_code = encode(db_url.id)
    db_url.short_code = short_code
    db.commit()

    return {"short_url": f"{BASE_URL}/{short_code}"}


@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.clicks += 1
    db.commit()

    return RedirectResponse(url.original_url)


@router.get("/stats/{short_code}", response_model=schemas.URLStats)
def get_stats(short_code: str, db: Session = Depends(get_db)):

    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return url
