import subprocess
import sys
from setuptools import setup, find_packages

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

setup(
    name="PDF to Audiobook Converter",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'PyPDF2',
        'gTTS',
        'pydub',
        'PySimpleGUI',
        'torch',
        'TTS',
        'tqdm'
    ],
)

# Install ffmpeg
try:
    subprocess.check_call(['ffmpeg', '-version'])
except:
    if sys.platform.startswith('darwin'):  # macOS
        subprocess.check_call(['brew', 'install', 'ffmpeg'])
    elif sys.platform.startswith('linux'):  # Linux
        subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'])
    elif sys.platform.startswith('win'):  # Windows
        print("Please install ffmpeg manually from https://ffmpeg.org/download.html")
    else:
        print("Unsupported operating system. Please install ffmpeg manually.")

print("Setup complete! You can now run the application using 'python gui.py' or 'python pdf_to_audiobook.py'")