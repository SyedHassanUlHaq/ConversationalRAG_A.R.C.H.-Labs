#!/usr/bin/env python3
"""
Test OpenAI API key
"""

import os
from dotenv import load_dotenv

def test_openai():
    """Test if OpenAI API key works"""
    try:
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ OpenAI API key not configured")
            print("Please add OPENAI_API_KEY=your_key_here to .env file")
            return False
            
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OpenAI is working!'"}],
            max_tokens=50
        )
        
        print("✅ OpenAI API is working!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔑 Testing OpenAI API Key...")
    test_openai() 