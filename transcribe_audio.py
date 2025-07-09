#!/usr/bin/env python3
"""
Audio Transcription Script using Google Gemini 2.5 Pro
Transcribes audio files from the Audio folder and saves them as text files.
"""

import os
import base64
import mimetypes
import os
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
        
        # Default transcription prompt (fallback)
        self.default_prompt = """
        Please transcribe the audio content accurately. 
        Include proper punctuation and formatting.
        If there are multiple speakers, indicate speaker changes.
        Provide a clear, readable transcription of the spoken content.
        """
        
        # Load transcription prompt from file or user selection
        self.transcription_prompt = self.select_prompt()
    
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
                    max_output_tokens=65536,
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
    
    def get_available_prompts(self, prompts_folder="prompts"):
        """
        Get all available prompt files from the prompts folder.
        
        Args:
            prompts_folder (str): Path to the prompts folder
            
        Returns:
            list: List of tuples (number, description, filepath)
        """
        prompts_path = Path(prompts_folder)
        if not prompts_path.exists():
            print(f"Warning: Prompts folder '{prompts_folder}' not found.")
            return []
        
        prompt_files = []
        for file_path in prompts_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == '.md':
                # Extract description from filename (remove number prefix and extension)
                name_part = file_path.stem
                if '_' in name_part:
                    number_part, description = name_part.split('_', 1)
                    try:
                        number = int(number_part)
                        description = description.replace('_', ' ').title()
                        prompt_files.append((number, description, file_path))
                    except ValueError:
                        # If no number prefix, use filename as description
                        description = name_part.replace('_', ' ').title()
                        prompt_files.append((0, description, file_path))
                else:
                    description = name_part.replace('_', ' ').title()
                    prompt_files.append((0, description, file_path))
        
        return sorted(prompt_files, key=lambda x: x[0])
    
    def display_prompt_menu(self, available_prompts):
        """
        Display the prompt selection menu.
        
        Args:
            available_prompts (list): List of available prompts
        """
        print("\n" + "=" * 50)
        print("PROMPT SELECTION")
        print("=" * 50)
        print("Available transcription prompts:")
        print()
        
        for number, description, _ in available_prompts:
            if number > 0:
                print(f"{number}. {description}")
            else:
                print(f"   {description}")
        
        print()
    
    def load_prompt_content(self, prompt_file_path):
        """
        Load prompt content from a markdown file.
        
        Args:
            prompt_file_path (Path): Path to the prompt file
            
        Returns:
            str: The prompt content or default prompt if error
        """
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract content after the first markdown header
            lines = content.split('\n')
            prompt_lines = []
            found_header = False
            
            for line in lines:
                if line.startswith('# ') and not found_header:
                    found_header = True
                    continue
                elif found_header and line.strip():
                    prompt_lines.append(line)
            
            if prompt_lines:
                return '\n'.join(prompt_lines).strip()
            else:
                return content.strip()
                
        except Exception as e:
            print(f"Error loading prompt from '{prompt_file_path}': {e}")
            return self.default_prompt
    
    def select_prompt(self, prompts_folder="prompts"):
        """
        Allow user to select a transcription prompt.
        
        Args:
            prompts_folder (str): Path to the prompts folder
            
        Returns:
            str: Selected prompt content
        """
        available_prompts = self.get_available_prompts(prompts_folder)
        
        if not available_prompts:
            print("No prompt files found. Using default prompt.")
            return self.default_prompt
        
        # Display menu
        self.display_prompt_menu(available_prompts)
        
        # Get user selection
        numbered_prompts = [(num, desc, path) for num, desc, path in available_prompts if num > 0]
        
        if not numbered_prompts:
            print("No numbered prompts found. Using default prompt.")
            return self.default_prompt
        
        while True:
            try:
                choice = input(f"Select a prompt (1-{len(numbered_prompts)}) or press Enter for default: ").strip()
                
                if not choice:
                    print("Using default prompt.")
                    return self.default_prompt
                
                choice_num = int(choice)
                
                # Find the prompt with the selected number
                selected_prompt = None
                for num, desc, path in numbered_prompts:
                    if num == choice_num:
                        selected_prompt = (num, desc, path)
                        break
                
                if selected_prompt:
                    _, description, prompt_path = selected_prompt
                    print(f"Selected: {description}")
                    return self.load_prompt_content(prompt_path)
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(numbered_prompts)}.")
                    
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nUsing default prompt.")
                return self.default_prompt

def main():
    """
    Main function to run the audio transcription script.
    """
    print("Audio Transcription using Google Gemini 2.5 Pro")
    print("=" * 50)
    
    try:
        # Initialize transcriber (prompt will be loaded from prompt_template.md)
        transcriber = AudioTranscriber()
        
        # Transcribe all audio files using the prompt from the template file
        transcriber.transcribe_all_audio_files(
            audio_folder="Audio",
            output_folder="Transcriptions"
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
