#!/usr/bin/env python3
"""
Test script to verify Gemini API connection and functionality.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

def test_api_connection():
    """Test the Gemini API connection."""
    
    print("Testing Gemini API Connection...")
    print("=" * 40)
    
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found!")
        print("\nTo set your API key:")
        print("1. Edit the .env file in this directory")
        print("2. Replace 'your-api-key-here' with your actual API key")
        print("3. Save the file and run this script again")
        return False
    
    print("✅ API key found in environment variables")
    
    try:
        # Initialize client
        client = genai.Client(api_key=api_key)
        print("✅ Gemini client initialized successfully")
        
        # Test with a simple text request
        print("\nTesting text generation...")
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents='Say "Hello, I am Gemini 2.5 Pro and I am ready to transcribe audio!"',
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=50
            )
        )
        
        print("✅ API test successful!")
        print(f"Response: {response.text}")
        
        # List available models
        print("\nChecking available models...")
        try:
            models = list(client.models.list())
            gemini_models = [model for model in models if 'gemini' in model.name.lower()]
            print(f"✅ Found {len(gemini_models)} Gemini model(s)")
            for model in gemini_models[:3]:  # Show first 3
                print(f"   - {model.name}")
        except Exception as e:
            print(f"⚠️  Could not list models: {e}")
        
        print("\n🎉 All tests passed! You're ready to transcribe audio files.")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nPossible issues:")
        print("- Invalid API key")
        print("- Network connection problems")
        print("- API quota exceeded")
        return False

def main():
    """Main function."""
    print("Gemini API Test Script")
    print("=" * 40)
    
    success = test_api_connection()
    
    if success:
        print("\nYou can now run:")
        print("python transcribe_audio.py")
    else:
        print("\nPlease fix the issues above before proceeding.")

if __name__ == "__main__":
    main()
