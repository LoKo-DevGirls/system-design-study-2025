from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timedelta
import validators
import secrets
import string
from typing import Optional, List
import os
import qrcode
import io
import base64

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./url_shortener.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    click_count = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    title = Column(String, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class URLShortenRequest(BaseModel):
    url: HttpUrl
    custom_alias: Optional[str] = None
    expires_in_days: Optional[int] = None
    title: Optional[str] = None

class BulkURLRequest(BaseModel):
    urls: List[HttpUrl]
    expires_in_days: Optional[int] = None

class URLResponse(BaseModel):
    short_url: str
    original_url: str
    click_count: int
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool
    title: Optional[str] = None
    qr_code: Optional[str] = None

class BulkURLResponse(BaseModel):
    results: List[URLResponse]
    total_created: int
    errors: List[str] = []

# FastAPI app
app = FastAPI(title="URL Shortener", description="A modern URL shortener service")

# Templates
templates = Jinja2Templates(directory="templates")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def generate_short_code(length: int = 6) -> str:
    """Generate a random short code"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def is_valid_url(url: str) -> bool:
    """Validate if the URL is properly formatted"""
    return validators.url(url)

def generate_qr_code(url: str) -> str:
    """Generate QR code for the URL and return as base64 string"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def is_url_expired(url_record: URL) -> bool:
    """Check if URL has expired"""
    if not url_record.expires_at:
        return False
    return datetime.utcnow() > url_record.expires_at

# API Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/shorten", response_model=URLResponse)
async def shorten_url(request: URLShortenRequest, db: Session = Depends(get_db)):
    """Create a short URL"""
    
    # Validate URL
    if not is_valid_url(str(request.url)):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    # Check if custom alias is provided
    if request.custom_alias:
        # Check if custom alias already exists
        existing_url = db.query(URL).filter(URL.short_code == request.custom_alias).first()
        if existing_url:
            raise HTTPException(status_code=400, detail="Custom alias already exists")
        short_code = request.custom_alias
    else:
        # Generate unique short code
        while True:
            short_code = generate_short_code()
            existing_url = db.query(URL).filter(URL.short_code == short_code).first()
            if not existing_url:
                break
    
    # Calculate expiration date
    expires_at = None
    if request.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=request.expires_in_days)
    
    # Create new URL record
    db_url = URL(
        short_code=short_code,
        original_url=str(request.url),
        expires_at=expires_at,
        title=request.title
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    # Generate QR code
    short_url = f"http://localhost:8000/{short_code}"
    qr_code = generate_qr_code(short_url)
    
    return URLResponse(
        short_url=short_url,
        original_url=str(request.url),
        click_count=0,
        created_at=db_url.created_at,
        expires_at=expires_at,
        is_active=True,
        title=request.title,
        qr_code=qr_code
    )

@app.get("/{short_code}")
async def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """Redirect to the original URL"""
    url_record = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not url_record:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Check if URL is active and not expired
    if not url_record.is_active:
        raise HTTPException(status_code=410, detail="URL has been deactivated")
    
    if is_url_expired(url_record):
        raise HTTPException(status_code=410, detail="URL has expired")
    
    # Increment click count
    url_record.click_count += 1
    db.commit()
    
    return RedirectResponse(url=url_record.original_url)

@app.get("/api/stats/{short_code}", response_model=URLResponse)
async def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    """Get statistics for a short URL"""
    url_record = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not url_record:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Generate QR code
    short_url = f"http://localhost:8000/{url_record.short_code}"
    qr_code = generate_qr_code(short_url)
    
    return URLResponse(
        short_url=short_url,
        original_url=url_record.original_url,
        click_count=url_record.click_count,
        created_at=url_record.created_at,
        expires_at=url_record.expires_at,
        is_active=url_record.is_active,
        title=url_record.title,
        qr_code=qr_code
    )

@app.post("/api/bulk-shorten", response_model=BulkURLResponse)
async def bulk_shorten_urls(request: BulkURLRequest, db: Session = Depends(get_db)):
    """Create multiple short URLs at once"""
    results = []
    errors = []
    
    for url in request.urls:
        try:
            # Validate URL
            if not is_valid_url(str(url)):
                errors.append(f"Invalid URL format: {url}")
                continue
            
            # Generate unique short code
            while True:
                short_code = generate_short_code()
                existing_url = db.query(URL).filter(URL.short_code == short_code).first()
                if not existing_url:
                    break
            
            # Calculate expiration date
            expires_at = None
            if request.expires_in_days:
                expires_at = datetime.utcnow() + timedelta(days=request.expires_in_days)
            
            # Create new URL record
            db_url = URL(
                short_code=short_code,
                original_url=str(url),
                expires_at=expires_at
            )
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            
            # Generate QR code
            short_url = f"http://localhost:8000/{short_code}"
            qr_code = generate_qr_code(short_url)
            
            results.append(URLResponse(
                short_url=short_url,
                original_url=str(url),
                click_count=0,
                created_at=db_url.created_at,
                expires_at=expires_at,
                is_active=True,
                qr_code=qr_code
            ))
            
        except Exception as e:
            errors.append(f"Error processing {url}: {str(e)}")
    
    return BulkURLResponse(
        results=results,
        total_created=len(results),
        errors=errors
    )

@app.delete("/api/deactivate/{short_code}")
async def deactivate_url(short_code: str, db: Session = Depends(get_db)):
    """Deactivate a short URL"""
    url_record = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not url_record:
        raise HTTPException(status_code=404, detail="URL not found")
    
    url_record.is_active = False
    db.commit()
    
    return {"message": "URL deactivated successfully"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "URL Shortener is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
