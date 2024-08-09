import os
import argparse
from PyPDF2 import PdfReader
from gtts import gTTS
from pydub import AudioSegment
import tempfile

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    return tts

def save_audiobook(audio, output_path):
    audio.save(output_path)

def process_large_text(text, lang='en', chunk_size=5000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    audio_chunks = []

    for chunk in chunks:
        tts = text_to_speech(chunk, lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            tts.save(temp_file.name)
            audio_chunk = AudioSegment.from_mp3(temp_file.name)
            audio_chunks.append(audio_chunk)
        os.unlink(temp_file.name)

    return sum(audio_chunks)

def pdf_to_audiobook(pdf_path, output_path, lang='en'):
    text = extract_text_from_pdf(pdf_path)
    audio = process_large_text(text, lang)
    audio.export(output_path, format="mp3")

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Audiobook")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("output_path", help="Path to save the output audio file")
    parser.add_argument("--lang", default="en", help="Language code (e.g., 'en' for English, 'es' for Spanish)")

    args = parser.parse_args()

    try:
        pdf_to_audiobook(args.pdf_path, args.output_path, args.lang)
        print(f"Audiobook successfully created and saved to {args.output_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()