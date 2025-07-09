# Audio Transcription with Google Gemini 2.5 Pro

This project provides a Python script to transcribe audio files using Google's Gemini 2.5 Pro model.

## Features

- Transcribes various audio formats (MP3, WAV, M4A, FLAC, OGG, WebM, MP4, AAC)
- Uses Google Gemini 2.5 Pro for accurate transcription
- **Interactive prompt selection** - Choose from specialized transcription styles
- Automatically saves transcriptions as text files
- Handles multiple speakers and provides formatted output
- Batch processing of multiple audio files
- Customizable prompts for different content types

## Setup

### 1. Install Dependencies

```bash
pip install google-genai python-dotenv
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Configure Your API Key

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
3. Edit the `.env` file and replace `your-api-key-here` with your actual API key:

```env
GEMINI_API_KEY=your-actual-api-key-here
```

**Security Note**: The `.env` file is included in `.gitignore` to prevent accidentally committing your API key to version control.

### 3. Add Audio Files

Place your audio files in the `Audio` folder. Supported formats:
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)
- WebM (.webm)
- MP4 (.mp4)
- AAC (.aac)

## Usage

Run the main transcription script:

```bash
python transcribe_audio.py
```

When you run the script, you'll be prompted to select a transcription style:

```
PROMPT SELECTION
==================================================
Available transcription prompts:

1. General
2. Meeting  
3. Interview
4. Lecture
5. Technical
6. Medical
7. Legal

Select a prompt (1-7) or press Enter for default:
```

The script will then:
1. Use your selected prompt style for transcription
2. Find all supported audio files in the `Audio` folder
3. Transcribe each file using Gemini 2.5 Pro
4. Save transcriptions in the `Transcriptions` folder

## Output

Transcriptions are saved as `.txt` files in the `Transcriptions` folder with the format:
- Original file: `audio_recording.mp3`
- Transcription: `audio_recording_transcription.txt`

Each transcription file includes:
- Header with original filename
- Metadata about the transcription process
- The actual transcribed text

## Customization

### Prompt Selection
The script includes several pre-built transcription prompts optimized for different use cases:

- **General**: Standard transcription with speaker identification
- **Meeting**: Focus on action items, decisions, and meeting structure  
- **Interview**: Question-answer format with conversational flow
- **Lecture**: Educational content with key concepts highlighted

### Adding Custom Prompts
To add your own custom prompt:

1. Create a new `.md` file in the `prompts` folder
2. Name it with a number prefix: `8_custom.md`
3. Add your prompt content after a markdown header
4. The script will automatically detect and offer it as an option

Example custom prompt file (`prompts/8_podcast.md`):
```markdown
# Podcast Transcription Prompt

Please transcribe this podcast accurately.
- Identify hosts and guests clearly
- Include intro/outro music notes in [brackets]
- Maintain the casual, conversational tone
- Note any sponsor mentions or advertisements
- Include audience engagement (laughs, applause) in [brackets]
```

### Advanced Customization
You can also modify existing prompts by editing the files in the `prompts` folder, or pass a custom prompt directly in the code.

## File Structure

```
Audio-transcription/
├── Audio/                    # Place your audio files here
├── Transcriptions/          # Generated transcriptions appear here
├── prompts/                 # Transcription prompt templates
│   ├── 1_general.md        # General transcription prompt
│   ├── 2_meeting.md        # Meeting-focused prompt
│   ├── 3_interview.md      # Interview-style prompt
│   ├── 4_lecture.md        # Educational content prompt
├── .env                     # Your API key configuration (create from .env.example)
├── .env.example            # Template for environment variables
├── .gitignore              # Prevents sensitive files from being committed
├── transcribe_audio.py     # Main transcription script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Troubleshooting

### API Key Issues
- Make sure your `GEMINI_API_KEY` environment variable is set
- Verify your API key is valid and has proper permissions

### Audio Format Issues
- Ensure your audio files are in supported formats
- Check file permissions and accessibility

### Large Files
- Gemini 2.5 Pro has file size limits
- Consider breaking large audio files into smaller segments

## API Reference

Using the latest Google GenAI Python SDK (v1.24.0+) with Gemini 2.5 Pro model.

Key components:
- `genai.Client()` - Initialize the Gemini client
- `types.Part.from_bytes()` - Create audio parts from file data
- `client.models.generate_content()` - Generate transcriptions

## License

This project is open source. Please ensure you comply with Google's API terms of service when using the Gemini API.
