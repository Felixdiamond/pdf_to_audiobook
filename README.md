# PDF to Audiobook Converter

This Python application converts PDF files to audiobooks using Text-to-Speech (TTS) technology. It features a modern, user-friendly graphical interface and supports multiple languages.

## Features

- Convert PDF files to MP3 audiobooks
- Support for multiple languages
- Efficient processing of large PDF files
- Modern and intuitive graphical user interface
- Command-line interface option
- Dark mode for comfortable use

## Requirements

- Python 3.6+
- ffmpeg
- eSpeak
- PyPDF2
- gTTS (Google Text-to-Speech)
- pydub
- CustomTkinter
- Coqui TTS (for advanced TTS options)

## Installation

1. Clone this repository or download the scripts.

2. Install system dependencies:
   - On Ubuntu/Debian:
     ```
     sudo apt-get update
     sudo apt-get install -y ffmpeg espeak
     ```
   - On macOS (using Homebrew):
     ```
     brew install ffmpeg espeak
     ```
   - On Windows:
     - Install ffmpeg: https://ffmpeg.org/download.html
     - Install eSpeak: http://espeak.sourceforge.net/download.html

3. Run the setup script to install all required Python dependencies:

   ```
   python setup.py install
   ```

   This will install all necessary Python packages and set up the application.

## Usage

### Graphical User Interface

To use the GUI version of the application, run:

```
python gui.py
```

This will open a sleek, modern interface where you can:
- Select your PDF file
- Choose the output MP3 file location
- Select the language for text-to-speech
- Adjust the chunk size for processing
- Start the conversion process with a single click

### Command-line Interface

You can also run the script from the command line with the following syntax:

```
python pdf_to_audiobook.py <input_pdf> <output_mp3> [--lang <language_code>] [--chunk_size <size>] [--max_decoder_steps <steps>]
```

Arguments:
- `<input_pdf>`: Path to the input PDF file
- `<output_mp3>`: Path where the output MP3 file will be saved
- `--lang`: (Optional) Language code for TTS (default is 'en' for English)
- `--chunk_size`: (Optional) Size of text chunks to process (default is 500)
- `--max_decoder_steps`: (Optional) Maximum decoder steps for Coqui TTS (default is 1000000)

Example:
```
python pdf_to_audiobook.py my_book.pdf my_audiobook.mp3 --lang es --chunk_size 1000
```

## Troubleshooting

If you encounter any issues during installation or running the application:

1. Ensure all system dependencies (ffmpeg and espeak) are correctly installed for your operating system.
2. Check that your Python version is 3.6 or higher.
3. If you're having issues with a specific Python package, try installing it manually using pip:
   ```
   pip install package_name
   ```
4. For GUI issues, ensure CustomTkinter is properly installed:
   ```
   pip install customtkinter
   ```

## Supported Languages

The application supports a wide range of languages, including but not limited to:

- English ('en')
- Spanish ('es')
- French ('fr')
- German ('de')
- Italian ('it')
- Portuguese ('pt')
- Chinese ('zh-cn')
- Japanese ('ja')

The exact list of supported languages may vary depending on the TTS engine used (gTTS or Coqui TTS).

## Contributing

Contributions to improve the application are welcome. Please feel free to submit a Pull Request.