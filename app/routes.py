from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas
from .base62 import encode
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Dashboard Home
@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    urls = db.query(models.URL).order_by(models.URL.id.desc()).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "urls": urls}
    )


# 🔹 Form-based Shorten (Dashboard)
@router.post("/shorten")
def create_short_url_form(original_url: str = Form(...), db: Session = Depends(get_db)):

    db_url = models.URL(original_url=original_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    short_code = encode(db_url.id)
    db_url.short_code = short_code
    db.commit()

    return RedirectResponse(url="/", status_code=303)


# 🔹 JSON API Shorten (Keep API support)
@router.post("/api/shorten", response_model=schemas.URLResponse)
def create_short_url_api(url: schemas.URLCreate, db: Session = Depends(get_db)):

    db_url = models.URL(original_url=url.original_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    short_code = encode(db_url.id)
    db_url.short_code = short_code
    db.commit()

    return {"short_url": f"{BASE_URL}/{short_code}"}


# 🔹 Redirect
@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.clicks += 1
    db.commit()

    return RedirectResponse(url.original_url)


# 🔹 Stats Page (HTML)
@router.get("/stats/{short_code}")
def stats(request: Request, short_code: str, db: Session = Depends(get_db)):

    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return templates.TemplateResponse(
        "stats.html",
        {"request": request, "url": url}
    )
