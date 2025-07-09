# Audio Transcription with Google Gemini 2.5 Pro

This project provides two ways to transcribe audio files using Google's Gemini 2.5 Pro model:

## 🚀 Quick Start Options

### Option 1: Google Colab (Recommended for beginners)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fmadore/Audio-transcription/blob/main/Audio_Transcription_Colab.ipynb)

**No setup required!** Click the button above to start transcribing immediately in your browser.

- ✅ **Works anywhere** - No installation needed
- ✅ **Cross-platform** - Windows, Mac, Linux, mobile
- ✅ **Interactive interface** - User-friendly widgets
- ✅ **Secure** - Your API key stays private

### Option 2: Local Python Script
For developers who prefer running locally or need automation.

## Features

- Transcribes various audio formats (MP3, WAV, M4A, FLAC, OGG, WebM, MP4, AAC)
- Uses Google Gemini 2.5 Pro for accurate transcription
- **Interactive prompt selection** - Choose from 7 specialized transcription styles
- Automatically saves transcriptions as text files
- Handles multiple speakers and provides formatted output
- Batch processing of multiple audio files
- Customizable prompts for different content types

## 🎯 Transcription Styles

Both versions offer specialized prompts optimized for different content types:

- **General** - Standard transcription with speaker identification
- **Meeting** - Business meetings with action items and decisions
- **Interview** - Q&A format with conversational flow
- **Lecture** - Educational content with key concepts
- **Technical** - Precise terminology and specifications
- **Medical** - Healthcare terminology and clinical accuracy
- **Legal** - Formal language and legal terminology

## 🔧 Local Setup (Option 2)

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

## 📋 Usage

### Google Colab Version
1. Click the "Open in Colab" badge at the top
2. Follow the step-by-step notebook cells
3. Upload your audio files directly in the browser
4. Download transcriptions with one click

### Local Python Script
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
├── Audio_Transcription_Colab.ipynb  # Google Colab notebook
├── README_Colab.md         # Colab-specific documentation
├── setup_github.py         # GitHub deployment script
└── README.md              # This file
```

## 🚀 Deploy Your Own Colab Version

Want to create your own GitHub repository with the Colab notebook? Use our automated setup script:

### Prerequisites
1. **Git** - [Download here](https://git-scm.com/downloads)
2. **GitHub CLI** - [Download here](https://cli.github.com/)
3. **GitHub account** - [Sign up here](https://github.com/)

### Quick Setup
```bash
# 1. Clone this repository
git clone https://github.com/your-username/Audio-transcription.git
cd Audio-transcription

# 2. Authenticate with GitHub
gh auth login

# 3. Run the setup script
python setup_github.py
```

The script will:
- ✅ Create a new GitHub repository
- ✅ Copy the Colab notebook and documentation
- ✅ Update all links with your repository information
- ✅ Push everything to GitHub
- ✅ Provide your custom Colab link

### Windows Users
Double-click `setup_github.bat` for a guided setup experience.

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

### Colab Issues
- **Runtime disconnected**: Restart runtime and re-run setup cells
- **API quota exceeded**: Check your Gemini API usage limits
- **File upload fails**: Try smaller files or refresh the page

## API Reference

Using the latest Google GenAI Python SDK (v1.24.0+) with Gemini 2.5 Pro model.

Key components:
- `genai.Client()` - Initialize the Gemini client
- `types.Part.from_bytes()` - Create audio parts from file data
- `client.models.generate_content()` - Generate transcriptions

## License

This project is open source. Please ensure you comply with Google's API terms of service when using the Gemini API.
