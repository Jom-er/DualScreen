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

## Building Executable (.exe for Windows)

To create a standalone .exe file for Windows:

### Method 1: Using PyInstaller

1. **On Windows**, install Python and dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```bash
   pyinstaller DualScreen.spec
   ```
   Or manually:
   ```bash
   pyinstaller --onefile --windowed --hidden-import PyQt5.QtCore --hidden-import PyQt5.QtGui --hidden-import PyQt5.QtWidgets --hidden-import mss --hidden-import pyaudio --hidden-import ffmpeg --hidden-import numpy --hidden-import cv2 main.py
   ```

3. **Find the .exe**: In the `dist` folder as `DualScreen.exe`.

### Method 2: Using auto-py-to-exe (GUI)

1. Install auto-py-to-exe:
   ```bash
   pip install auto-py-to-exe
   ```

2. Run:
   ```bash
   auto-py-to-exe
   ```

3. In the GUI:
   - Script location: Select `main.py`
   - One file: Yes
   - Windowed: Yes
   - Add hidden imports: PyQt5.QtCore, PyQt5.QtGui, PyQt5.QtWidgets, mss, pyaudio, ffmpeg, numpy, cv2
   - Convert

### Method 3: Using cx_Freeze

1. Install cx_Freeze:
   ```bash
   pip install cx-Freeze
   ```

2. Run:
   ```bash
   python setup.py build
   ```

The executable will be in `build/exe.win-amd64-3.x/` or similar.

### Requirements for Building

- Python 3.6+ on Windows
- All dependencies from requirements.txt
- ffmpeg installed and in PATH (download from https://ffmpeg.org/)
- Microsoft Visual C++ Redistributable if needed

### Note

Building on Linux (like Codespaces) creates Linux executables, not .exe. You must build on Windows to get a .exe file.

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
