#!/bin/bash

echo "🚀 Starting URL Shortener - NeetCodeIO Style"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Start the application
echo
echo "🎯 Starting the application..."
echo "📱 Open your browser to: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo
python3 run.py
