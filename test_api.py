#!/usr/bin/env python3
"""
Simple script to test Google AI API key
"""

import os
from dotenv import load_dotenv

def test_api_key():
    """Test if the Google AI API key works"""
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key or api_key in ['your_google_ai_api_key_here', 'YOUR_ACTUAL_API_KEY_HERE']:
            print("❌ API key not configured properly")
            print("Please edit .env file and add your real Google AI API key")
            return False
        
        # Test the API
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'Hello, API is working!'")
        
        print("✅ API key is working!")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔑 Testing Google AI API Key...")
    test_api_key() 