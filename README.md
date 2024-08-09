# PDF to Audiobook Converter

This Python script converts PDF files to audiobooks using Text-to-Speech (TTS) technology. It's designed to be robust, user-friendly, and multilingual.

## Features

- Convert PDF files to MP3 audiobooks
- Support for multiple languages
- Efficient processing of large PDF files
- User-friendly command-line interface
- Error handling for smooth operation

## Requirements

- Python 3.6+
- PyPDF2
- gTTS (Google Text-to-Speech)
- pydub

## Installation

1. Clone this repository or download the script.

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3. Ensure you have ffmpeg and eSpeak installed on your system.

## Usage

Run the script from the command line with the following syntax:

```
python pdf_to_audiobook.py <input_pdf> <output_mp3> [--lang <language_code>]
```

Arguments:
- `<input_pdf>`: Path to the input PDF file
- `<output_mp3>`: Path where the output MP3 file will be saved
- `--lang`: (Optional) Language code for TTS (default is 'en' for English)

Example:
```
python pdf_to_audiobook.py my_book.pdf my_audiobook.mp3 --lang es
```

This command will convert `my_book.pdf` to `my_audiobook.mp3` using Spanish ('es') as the language for text-to-speech.

## Supported Languages

The script supports all languages available in the gTTS library. Some common language codes include:

- 'en' (English)
- 'es' (Spanish)
- 'fr' (French)
- 'de' (German)
- 'it' (Italian)
- 'ja' (Japanese)
- 'ko' (Korean)
- 'zh-CN' (Chinese, Simplified) the PDF

## Contributing

Contributions to improve the script are welcome. Please feel free to submit a Pull Request.
