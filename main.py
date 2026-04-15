#!/usr/bin/env python3
"""
DualScreen - A simple screen recorder with GUI
"""

import sys
import os

def main():
    # Check if display is available
    if not os.environ.get('DISPLAY'):
        print("No display available. This application requires a graphical environment.")
        print("Please run this on a system with a display server (X11, Wayland, etc.).")
        print("In Codespaces, you can run it locally after cloning the repository.")
        return

    try:
        from PyQt5.QtWidgets import QApplication
        from gui import ScreenRecorderGUI

        app = QApplication(sys.argv)
        app.setApplicationName("DualScreen")
        app.setApplicationVersion("1.0")

        window = ScreenRecorderGUI()
        window.show()

        sys.exit(app.exec_())
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all dependencies are installed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()