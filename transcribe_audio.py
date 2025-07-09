#!/usr/bin/env python3
"""
Audio Transcription Script using Google Gemini 2.5 Pro
Transcribes audio files from the Audio folder and saves them as text files.
"""

import os
import base64
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

class AudioTranscriber:
    def __init__(self, api_key=None):
        """
        Initialize the Audio Transcriber with Gemini API.
        
        Args:
            api_key (str, optional): Gemini API key. If None, will use GEMINI_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file or environment variables")
        
        # Initialize the Gemini client
        self.client = genai.Client(api_key=self.api_key)
        
        # Supported audio formats
        self.supported_formats = {
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.m4a': 'audio/mp4',
            '.flac': 'audio/flac',
            '.ogg': 'audio/ogg',
            '.webm': 'audio/webm',
            '.mp4': 'audio/mp4',
            '.aac': 'audio/aac'
        }
        
        # Default transcription prompt
        self.transcription_prompt = """
        Please transcribe the audio content accurately. 
        Include proper punctuation and formatting.
        If there are multiple speakers, indicate speaker changes.
        Provide a clear, readable transcription of the spoken content.
        """
    
    def get_audio_files(self, audio_folder="Audio"):
        """
        Get all supported audio files from the specified folder.
        
        Args:
            audio_folder (str): Path to the audio folder
            
        Returns:
            list: List of audio file paths
        """
        audio_path = Path(audio_folder)
        if not audio_path.exists():
            print(f"Audio folder '{audio_folder}' not found!")
            return []
        
        audio_files = []
        for file_path in audio_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                audio_files.append(file_path)
        
        return sorted(audio_files)
    
    def prepare_audio_for_api(self, audio_file_path):
        """
        Prepare audio file for Gemini API by reading it as bytes.
        
        Args:
            audio_file_path (Path): Path to the audio file
            
        Returns:
            tuple: (audio_bytes, mime_type)
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            
            # Get MIME type
            file_extension = audio_file_path.suffix.lower()
            mime_type = self.supported_formats.get(file_extension)
            
            if not mime_type:
                # Fallback to mimetypes module
                mime_type, _ = mimetypes.guess_type(str(audio_file_path))
            
            return audio_bytes, mime_type
        
        except Exception as e:
            print(f"Error reading audio file {audio_file_path}: {e}")
            return None, None
    
    def transcribe_audio(self, audio_file_path, custom_prompt=None):
        """
        Transcribe a single audio file using Gemini 2.5 Pro.
        
        Args:
            audio_file_path (Path): Path to the audio file
            custom_prompt (str, optional): Custom transcription prompt
            
        Returns:
            str: Transcribed text or None if error
        """
        print(f"Transcribing: {audio_file_path.name}")
        
        # Prepare audio data
        audio_bytes, mime_type = self.prepare_audio_for_api(audio_file_path)
        if not audio_bytes or not mime_type:
            return None
        
        try:
            # Create audio part for the API
            audio_part = types.Part.from_bytes(
                data=audio_bytes,
                mime_type=mime_type
            )
            
            # Use custom prompt or default
            prompt = custom_prompt or self.transcription_prompt
            
            # Generate transcription using Gemini 2.5 Pro
            response = self.client.models.generate_content(
                model='gemini-2.5-pro',
                contents=[prompt, audio_part],
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Low temperature for more consistent transcription
                    max_output_tokens=4096,
                )
            )
            
            return response.text.strip()
        
        except Exception as e:
            print(f"Error transcribing {audio_file_path.name}: {e}")
            return None
    
    def save_transcription(self, transcription, audio_file_path, output_folder="Transcriptions"):
        """
        Save transcription to a text file.
        
        Args:
            transcription (str): Transcribed text
            audio_file_path (Path): Original audio file path
            output_folder (str): Output folder for transcriptions
        """
        # Create output folder if it doesn't exist
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        # Create output filename
        output_filename = audio_file_path.stem + "_transcription.txt"
        output_file_path = output_path / output_filename
        
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                # Write header with metadata
                f.write(f"Transcription of: {audio_file_path.name}\n")
                f.write(f"Generated using: Google Gemini 2.5 Pro\n")
                f.write("=" * 50 + "\n\n")
                f.write(transcription)
            
            print(f"Transcription saved: {output_file_path}")
            return output_file_path
        
        except Exception as e:
            print(f"Error saving transcription: {e}")
            return None
    
    def transcribe_all_audio_files(self, audio_folder="Audio", output_folder="Transcriptions", custom_prompt=None):
        """
        Transcribe all audio files in the specified folder.
        
        Args:
            audio_folder (str): Path to the audio folder
            output_folder (str): Output folder for transcriptions
            custom_prompt (str, optional): Custom transcription prompt
        """
        audio_files = self.get_audio_files(audio_folder)
        
        if not audio_files:
            print("No supported audio files found in the Audio folder.")
            print(f"Supported formats: {', '.join(self.supported_formats.keys())}")
            return
        
        print(f"Found {len(audio_files)} audio file(s) to transcribe:")
        for file_path in audio_files:
            print(f"  - {file_path.name}")
        
        print("\nStarting transcription process...\n")
        
        successful_transcriptions = 0
        failed_transcriptions = 0
        
        for audio_file in audio_files:
            try:
                transcription = self.transcribe_audio(audio_file, custom_prompt)
                
                if transcription:
                    output_file = self.save_transcription(transcription, audio_file, output_folder)
                    if output_file:
                        successful_transcriptions += 1
                    else:
                        failed_transcriptions += 1
                else:
                    failed_transcriptions += 1
                    
            except Exception as e:
                print(f"Unexpected error processing {audio_file.name}: {e}")
                failed_transcriptions += 1
            
            print()  # Add spacing between files
        
        # Summary
        print("=" * 50)
        print("TRANSCRIPTION SUMMARY")
        print("=" * 50)
        print(f"Total files processed: {len(audio_files)}")
        print(f"Successful transcriptions: {successful_transcriptions}")
        print(f"Failed transcriptions: {failed_transcriptions}")
        
        if successful_transcriptions > 0:
            print(f"\nTranscriptions saved in the '{output_folder}' folder.")


def main():
    """
    Main function to run the audio transcription script.
    """
    print("Audio Transcription using Google Gemini 2.5 Pro")
    print("=" * 50)
    
    try:
        # Initialize transcriber
        transcriber = AudioTranscriber()
        
        # You can customize the transcription prompt here
        custom_prompt = """
        Please provide an accurate transcription of this audio file.
        Format the text with proper punctuation, capitalization, and paragraph breaks.
        If there are multiple speakers, please indicate speaker changes with "Speaker 1:", "Speaker 2:", etc.
        If you hear background music or sound effects, you may mention them in [brackets].
        Focus on clarity and readability of the final transcript.
        """
        
        # Transcribe all audio files
        transcriber.transcribe_all_audio_files(
            audio_folder="Audio",
            output_folder="Transcriptions",
            custom_prompt=custom_prompt
        )
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nTo use this script, you need to set your Gemini API key:")
        print("1. Get your API key from: https://makersuite.google.com/app/apikey")
        print("2. Edit the .env file in this directory")
        print("3. Replace 'your-api-key-here' with your actual API key")
        print("4. Save the file and run this script again")
        
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
