#!/usr/bin/env python3
"""
Test script for URL Shortener API
Run this to test all endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_shorten_url():
    """Test URL shortening"""
    print("🔗 Testing URL shortening...")
    
    # Test basic URL shortening
    data = {
        "url": "https://www.google.com/search?q=neetcode+url+shortener+tutorial"
    }
    
    response = requests.post(f"{BASE_URL}/api/shorten", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Short URL: {result['short_url']}")
        print(f"Original URL: {result['original_url']}")
        print(f"QR Code: {'Yes' if result['qr_code'] else 'No'}")
        return result['short_url'].split('/')[-1]  # Return short code
    else:
        print(f"Error: {response.json()}")
        return None

def test_custom_alias():
    """Test custom alias"""
    print("🏷️ Testing custom alias...")
    
    data = {
        "url": "https://github.com/neetcode-io",
        "custom_alias": "neetcode-github",
        "title": "NeetCode GitHub",
        "expires_in_days": 30
    }
    
    response = requests.post(f"{BASE_URL}/api/shorten", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Short URL: {result['short_url']}")
        print(f"Title: {result['title']}")
        print(f"Expires: {result['expires_at']}")
        return result['short_url'].split('/')[-1]
    else:
        print(f"Error: {response.json()}")
        return None

def test_redirect(short_code):
    """Test URL redirection"""
    if not short_code:
        print("❌ No short code to test redirect")
        return
        
    print(f"↗️ Testing redirect for {short_code}...")
    
    response = requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False)
    print(f"Status: {response.status_code}")
    print(f"Location: {response.headers.get('Location', 'N/A')}")
    print()

def test_stats(short_code):
    """Test statistics endpoint"""
    if not short_code:
        print("❌ No short code to test stats")
        return
        
    print(f"📊 Testing stats for {short_code}...")
    
    response = requests.get(f"{BASE_URL}/api/stats/{short_code}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Clicks: {result['click_count']}")
        print(f"Created: {result['created_at']}")
        print(f"Active: {result['is_active']}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_bulk_shorten():
    """Test bulk URL shortening"""
    print("📦 Testing bulk URL shortening...")
    
    data = {
        "urls": [
            "https://www.youtube.com/watch?v=qSJAvd5Mgio",
            "https://leetcode.com/problems/two-sum/",
            "https://github.com/neetcode-io/neetcode"
        ],
        "expires_in_days": 7
    }
    
    response = requests.post(f"{BASE_URL}/api/bulk-shorten", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total created: {result['total_created']}")
        print(f"Errors: {len(result['errors'])}")
        
        for i, url_result in enumerate(result['results']):
            print(f"  {i+1}. {url_result['short_url']}")
    else:
        print(f"Error: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("🧪 URL Shortener API Tests")
    print("=" * 40)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    try:
        # Test health
        test_health()
        
        # Test basic shortening
        short_code1 = test_shorten_url()
        print()
        
        # Test custom alias
        short_code2 = test_custom_alias()
        print()
        
        # Test redirect
        test_redirect(short_code1)
        test_redirect(short_code2)
        
        # Test stats
        test_stats(short_code1)
        test_stats(short_code2)
        
        # Test bulk shortening
        test_bulk_shorten()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()
