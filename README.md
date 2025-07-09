# Audio Transcription with Google Gemini 2.5 Pro

This project provides a Python script to transcribe audio files using Google's Gemini 2.5 Pro model.

## Features

- Transcribes various audio formats (MP3, WAV, M4A, FLAC, OGG, WebM, MP4, AAC)
- Uses Google Gemini 2.5 Pro for accurate transcription
- Automatically saves transcriptions as text files
- Handles multiple speakers and provides formatted output
- Batch processing of multiple audio files

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

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Edit the `.env` file in the project directory
3. Replace `your-api-key-here` with your actual API key:

```env
GEMINI_API_KEY=your-actual-api-key-here
```

**Note**: The `.env` file method is more secure and convenient than setting environment variables manually.

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

### Basic Usage

Run the main transcription script:

```bash
python transcribe_audio.py
```

This will:
1. Find all supported audio files in the `Audio` folder
2. Transcribe each file using Gemini 2.5 Pro
3. Save transcriptions in the `Transcriptions` folder

### Simple Example

For a basic implementation following your template:

```bash
python simple_transcribe.py
```

## Output

Transcriptions are saved as `.txt` files in the `Transcriptions` folder with the format:
- Original file: `audio_recording.mp3`
- Transcription: `audio_recording_transcription.txt`

Each transcription file includes:
- Header with original filename
- Metadata about the transcription process
- The actual transcribed text

## Customization

You can customize the transcription prompt by modifying the `custom_prompt` variable in the `main()` function of `transcribe_audio.py`.

Example custom prompts:
- For meetings: Focus on speaker identification and action items
- For interviews: Emphasize question-answer format
- For lectures: Focus on key concepts and structure

## File Structure

```
Audio-transcription/
├── Audio/                    # Place your audio files here
├── Transcriptions/          # Generated transcriptions appear here
├── transcribe_audio.py      # Main transcription script
├── simple_transcribe.py     # Simple example script
├── requirements.txt         # Python dependencies
└── README.md               # This file
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
