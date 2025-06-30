#!/usr/bin/env python3
"""
Setup script for Langchain Conversational RAG - Company Portfolio Assistant
"""

import os
import sys
from dotenv import load_dotenv

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import langchain
        import chainlit
        import google.generativeai as genai
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Please copy env.example to .env and add your Google API key")
        return False
    
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key or api_key == 'your_google_ai_api_key_here':
        print("❌ Google API key not configured")
        print("Please edit .env file and add your Google API key")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    print("✅ Environment file configured")
    return True

def test_api_connection():
    """Test connection to Google AI API"""
    try:
        load_dotenv()
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
        # Test basic API call
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, this is a test.")
        print("✅ Google AI API connection successful")
        return True
    except Exception as e:
        print(f"❌ Google AI API connection failed: {e}")
        print("Please check your API key and internet connection")
        return False

def test_data_loading():
    """Test if data loading works"""
    try:
        from chainlit_app import load_data
        docs = load_data()
        print(f"✅ Data loading successful - {len(docs)} document chunks loaded")
        
        # Show sample data
        if docs:
            print(f"Sample content: {docs[0].page_content[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("🚀 Langchain Conversational RAG Setup")
    print("=" * 60)
    
    steps = [
        ("Checking dependencies", check_dependencies),
        ("Checking environment file", check_env_file),
        ("Testing API connection", test_api_connection),
        ("Testing data loading", test_data_loading)
    ]
    
    all_passed = True
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\nYou can now run the application:")
        print("  Chainlit Web Interface: chainlit run chainlit_app.py -w")
        print("  Flask API: python app.py")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main() 