import base64
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

def generate():
    """Generate transcription for audio files using Gemini 2.5 Pro"""
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    
    # Example usage
    print("Audio Transcription Script Ready!")
    print("Make sure to set your GEMINI_API_KEY in the .env file.")

if __name__ == "__main__":
    generate()
