import os
import argparse
from PyPDF2 import PdfReader
from gtts import gTTS
from pydub import AudioSegment
import tempfile
from tqdm import tqdm
import torch
from TTS.api import TTS
import sys
from TTS.tts.configs.tacotron_config import TacotronConfig


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        total_pages = len(reader.pages)
        for page_num, page in enumerate(tqdm(reader.pages, desc="Extracting Text", total=total_pages, file=sys.stdout, dynamic_ncols=True)):
            text += page.extract_text()
            sys.stdout.flush()
    return text

def text_to_speech(text, lang='en', max_decoder_steps=100000):
    try:
        audio = text_to_speech_fastspeech2(text, lang, max_decoder_steps)
        print("Using FastSpeech2 TTS")
        return audio
    except Exception as e:
        print(f"FastSpeech2 TTS failed: {str(e)}. Falling back to Coqui TTS.")
        try:
            audio = text_to_speech_coqui(text, lang, max_decoder_steps)
            print("Using Coqui TTS")
            return audio
        except Exception as e:
            print(f"Coqui TTS failed: {str(e)}. Falling back to gTTS.")
            return text_to_speech_gtts(text, lang)

def text_to_speech_fastspeech2(text, lang='en', max_decoder_steps=5000):
    fastspeech2_lang_map = {
        'en': 'tts_models/en/ljspeech/fast_pitch',
        'zh-cn': 'tts_models/zh-CN/baker/fastspeech2',
        'ja': 'tts_models/ja/kokoro/fastspeech2',
        'es': 'tts_models/es/mai/tacotron2-DDC',
        'fr': 'tts_models/fr/mai/tacotron2-DDC',
        'de': 'tts_models/de/thorsten/tacotron2-DCA',
    }
    
    model_name = fastspeech2_lang_map.get(lang.lower(), fastspeech2_lang_map['en'])
    
    try:
        tts = TTS(model_name)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            tts.tts_to_file(text=text, file_path=temp_file.name)
            audio = AudioSegment.from_wav(temp_file.name)
        os.unlink(temp_file.name)
        return audio

    except Exception as e:
        print(f"Error with FastSpeech2 TTS for language {lang}: {str(e)}")
        raise

def text_to_speech_coqui(text, lang='en', max_decoder_steps=5000):
    lang_map = {
        'en': 'tts_models/en/vctk/vits',
        'es': 'tts_models/es/css10/vits',
        'fr': 'tts_models/fr/css10/vits',
        'de': 'tts_models/de/thorsten/vits',
        'it': 'tts_models/it/mai_female/vits',
        'pt': 'tts_models/pt/cv/vits',
        'pl': 'tts_models/pl/mai_female/vits',
        'tr': 'tts_models/tr/common-voice/vits',
        'ru': 'tts_models/ru/cv/vits',
        'nl': 'tts_models/nl/mai/vits',
        'cs': 'tts_models/cs/cv/vits',
        'ar': 'tts_models/ar/cv/vits',
        'zh-cn': 'tts_models/zh-CN/baker/vits',
        'ja': 'tts_models/ja/jsut/vits',
        'ko': 'tts_models/ko/cv/vits',
        'hi': 'tts_models/hi/cv/vits',
        'vi': 'tts_models/vi/vivos/vits',
        'uk': 'tts_models/uk/mai/vits'
    }
    model_name = lang_map.get(lang.lower(), lang_map['en'])
    
    try:
        tts = TTS(model_name)
        
        if 'tacotron' in model_name.lower():
            config = TacotronConfig()
            config.max_decoder_steps = max_decoder_steps
            tts.synthesizer.tts_model.decoder.max_decoder_steps = config.max_decoder_steps

        # Get available speakers for multi-speaker models
        speakers = tts.speakers if hasattr(tts, 'speakers') else None
        speaker = speakers[0] if speakers else None

        chunk_sizes = [len(text), len(text)//2, len(text)//4, len(text)//8]
        for chunk_size in chunk_sizes:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                    tts.tts_to_file(text=text[:chunk_size], file_path=temp_file.name, speaker=speaker)
                    audio = AudioSegment.from_wav(temp_file.name)
                os.unlink(temp_file.name)
                return audio
            except Exception as e:
                print(f"Failed with chunk size {chunk_size}: {str(e)}")
                if chunk_size == chunk_sizes[-1]:  
                    raise  

        raise Exception("Failed to synthesize speech with all chunk sizes")

    except Exception as e:
        print(f"Error with Coqui TTS for language {lang}: {str(e)}")
        raise

def text_to_speech_gtts(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        tts.save(temp_file.name)
        audio = AudioSegment.from_mp3(temp_file.name)
    os.unlink(temp_file.name)
    return audio

def save_audiobook(audio, output_path):
    audio.export(output_path, format="mp3")

def process_large_text(text, lang='en', chunk_size=500, max_decoder_steps=1000000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    audio_chunks = []
    total_chunks = len(chunks)
    
    for i, chunk in enumerate(tqdm(chunks, desc="Processing Text Chunks", total=total_chunks, file=sys.stdout, dynamic_ncols=True)):
        try:
            audio_chunk = text_to_speech_coqui(chunk, lang, max_decoder_steps)
            audio_chunks.append(audio_chunk)
        except Exception as e:
            print(f"Coqui TTS failed for chunk {i+1}/{total_chunks}: {str(e)}")
            print("Falling back to gTTS for this chunk")
            try:
                audio_chunk = text_to_speech_gtts(chunk, lang)
                audio_chunks.append(audio_chunk)
            except Exception as e:
                print(f"gTTS also failed for chunk {i+1}/{total_chunks}: {str(e)}")
                print("Skipping this chunk and continuing...")
        sys.stdout.flush()

    return sum(audio_chunks) if audio_chunks else None

def pdf_to_audiobook(pdf_path, output_path, lang='en', chunk_size=1000, max_decoder_steps=100000):
    print("Starting PDF to Audiobook conversion...")
    text = extract_text_from_pdf(pdf_path)
    print("Text extraction complete. Starting text-to-speech conversion...")
    audio = process_large_text(text, lang, chunk_size, max_decoder_steps)
    if audio:
        print("Text-to-speech conversion complete. Saving audiobook...")
        save_audiobook(audio, output_path)
        print(f"Audiobook successfully created and saved to {output_path}")
    else:
        print("Failed to generate audiobook: No audio was produced.")

def main(pdf_path, output_path, lang='en', chunk_size=1000, max_decoder_steps=100000):
    try:
        pdf_to_audiobook(pdf_path, output_path, lang, chunk_size, max_decoder_steps)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert PDF to Audiobook")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("output_path", help="Path to save the output audio file")
    parser.add_argument("--lang", default="en", help="Language code (e.g., 'en' for English, 'es' for Spanish)")
    parser.add_argument("--chunk_size", type=int, default=500, help="Size of text chunks to process")
    parser.add_argument("--max_decoder_steps", type=int, default=1000000, help="Maximum decoder steps for Coqui TTS")

    args = parser.parse_args()

    main(args.pdf_path, args.output_path, args.lang, args.chunk_size, args.max_decoder_steps)
