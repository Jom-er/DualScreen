# DualScreen - Screen Recorder

A simple screen recorder with a straightforward GUI, built in Python using PyQt5.

## Features

- Record your screen in MP4 with up to 120 FPS for ultra-smooth video
- Hardware Encoding (GPU acceleration) to minimize CPU load (software fallback)
- Capture system audio, microphone, or both (mic only in current version)
- Adjustable video quality and bitrate, supporting Constant Bitrate (CBR) and Variable Bitrate (VBR) up to 100mbps
- Save recordings directly to your chosen folder (.mp4 format)
- Automatically remembers your last settings
- Option to minimize to the tray while recording
- Supports video codecs like H.264 and H.265 (HEVC)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jom-er/DualScreen.git
   cd DualScreen
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install system dependencies (Ubuntu/Debian):
   ```bash
   sudo apt install portaudio19-dev ffmpeg libopencv-dev python3-pyqt5
   ```

## Download Windows Executable

A Windows .exe file is automatically built via GitHub Actions. To download:

1. Go to the [Actions tab](https://github.com/Jom-er/DualScreen/actions) on GitHub
2. Click on the latest "Build Windows Executable" workflow run
3. Download the "DualScreen-Windows" artifact (contains main.exe)

This .exe is standalone and includes all dependencies.

## Usage

Run the application:
```bash
python main.py
```

- Use the Record tab to start/stop recording and select output file.
- Use the Settings tab to adjust FPS, codec, bitrate, audio source, and other options.
- Settings are automatically saved.

## Requirements

- Python 3.6+
- PyQt5
- ffmpeg
- OpenCV
- PortAudio (for audio)

## Note

This application requires a graphical environment to run. It will not work in headless environments like GitHub Codespaces. Please run it on a local machine with a display.

## License

See LICENSE file.
