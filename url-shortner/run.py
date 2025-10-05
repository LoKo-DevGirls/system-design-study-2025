#!/usr/bin/env python3
"""
URL Shortener - NeetCodeIO Style
Run this script to start the application
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting URL Shortener...")
    print("📱 Open your browser to: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/api/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
