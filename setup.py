import subprocess
import sys
import platform
from setuptools import setup, find_packages

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_system_dependencies():
    system = platform.system().lower()
    if system == 'linux':
        try:
            subprocess.check_call(['sudo', 'apt-get', 'update'])
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'ffmpeg', 'espeak', 'python3-tk'])
        except subprocess.CalledProcessError:
            print("Error: Failed to install system dependencies. Please install ffmpeg, espeak, and python3-tk manually.")
    elif system == 'darwin':  # macOS
        try:
            subprocess.check_call(['brew', 'install', 'ffmpeg', 'espeak'])
            print("Please install Tkinter manually for macOS. You can download it from https://www.python.org/downloads/mac-osx/")
        except subprocess.CalledProcessError:
            print("Error: Failed to install system dependencies. Please install ffmpeg and espeak manually using Homebrew.")
    elif system == 'windows':
        print("For Windows, please manually install the following:")
        print("1. ffmpeg: https://ffmpeg.org/download.html")
        print("2. eSpeak: http://espeak.sourceforge.net/download.html")
        print("3. Tkinter should be included with your Python installation. If it's missing, consider reinstalling Python and select the option to install Tkinter.")
    else:
        print("Unsupported operating system. Please install ffmpeg, espeak, and Tkinter manually.")

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

if __name__ == "__main__":
    check_and_install_system_dependencies()
    print("\nInstalling Python dependencies...")
    for package in ['PyPDF2', 'gTTS', 'pydub', 'PySimpleGUI', 'torch', 'TTS', 'tqdm']:
        install(package)
    print("\nSetup complete! You can now run the application using 'python gui.py' or 'python pdf_to_audiobook.py'")
    print("\nNote: If you encounter any issues, please ensure that all system dependencies (ffmpeg, espeak, and Tkinter) are correctly installed for your operating system.")