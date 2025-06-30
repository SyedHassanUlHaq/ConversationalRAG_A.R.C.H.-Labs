#!/usr/bin/env python3
"""
Test Google AI Free Tier Setup
"""

import os
from dotenv import load_dotenv

def test_google_ai_free():
    """Test Google AI API with free tier"""
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("❌ No GOOGLE_API_KEY found in .env file")
            return False
            
        if len(api_key) != 39 or not api_key.startswith('AIzaSy'):
            print("❌ Google AI API key format looks incorrect")
            print(f"   Key length: {len(api_key)} (should be 39)")
            print(f"   Starts with: {api_key[:6]}... (should be AIzaSy)")
            return False
        
        print(f"✅ API key format looks correct: {api_key[:10]}...")
        
        # Test the API
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Use free tier model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            "Say 'Hello! Google AI Free Tier is working!'",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=50,
                temperature=0.7,
            )
        )
        
        print("✅ Google AI API is working!")
        print(f"✅ Test response: {response.text}")
        print("✅ Free tier setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Google AI: {str(e)}")
        if "quota" in str(e).lower():
            print("   This might be a quota issue. Try:")
            print("   1. Wait a few minutes and try again")
            print("   2. Create a new API key")
            print("   3. Enable billing (still free within limits)")
        return False

if __name__ == "__main__":
    test_google_ai_free() 