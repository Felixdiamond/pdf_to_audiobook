# PDF to Audiobook Converter

This Python application converts PDF files to audiobooks using Text-to-Speech (TTS) technology. It's designed to be robust, user-friendly, and multilingual, with both a command-line interface and a graphical user interface.

## Features

- Convert PDF files to MP3 audiobooks
- Support for multiple languages
- Efficient processing of large PDF files
- User-friendly command-line interface
- Sleek and modern graphical user interface
- Error handling for smooth operation

## Requirements

- Python 3.6+
- PyPDF2
- gTTS (Google Text-to-Speech)
- pydub
- PySimpleGUI (for GUI)
- Coqui TTS (for advanced TTS options)

## Installation

1. Clone this repository or download the scripts.

2. Run the setup script to install all required dependencies:

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

This will open a user-friendly interface where you can select your PDF file, choose output options, and convert to an audiobook with a click of a button.

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

This command will convert `my_book.pdf` to `my_audiobook.mp3` using Spanish ('es') as the language for text-to-speech and a chunk size of 1000.

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
- Korean ('ko')

The exact list of supported languages may vary depending on the TTS engine used (gTTS, Coqui TTS, or FastSpeech2).

## Contributing

Contributions to improve the application are welcome. Please feel free to submit a Pull Request.
