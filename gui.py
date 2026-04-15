from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QSpinBox, QComboBox, QCheckBox, QFileDialog,
    QSystemTrayIcon, QMenu, QAction, QMessageBox, QSlider, QGroupBox
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
import os
from recorder import ScreenRecorder
from settings import Settings

class ScreenRecorderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.recorder = ScreenRecorder()
        self.is_recording = False

        self.init_ui()
        self.init_tray()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle("DualScreen - Screen Recorder")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Record tab
        record_tab = QWidget()
        self.tabs.addTab(record_tab, "Record")

        record_layout = QVBoxLayout(record_tab)

        # Output file selection
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Output File:")
        self.output_edit = QLabel(self.get_default_output())
        self.output_button = QPushButton("Browse")
        self.output_button.clicked.connect(self.select_output)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.output_button)
        record_layout.addLayout(output_layout)

        # Record button
        self.record_button = QPushButton("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        record_layout.addWidget(self.record_button)

        # Status
        self.status_label = QLabel("Ready")
        record_layout.addWidget(self.status_label)

        # Settings tab
        settings_tab = QWidget()
        self.tabs.addTab(settings_tab, "Settings")

        settings_layout = QVBoxLayout(settings_tab)

        # FPS
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 120)
        fps_layout.addWidget(self.fps_spin)
        settings_layout.addLayout(fps_layout)

        # Codec
        codec_layout = QHBoxLayout()
        codec_layout.addWidget(QLabel("Codec:"))
        self.codec_combo = QComboBox()
        self.codec_combo.addItems(["h264", "h265"])
        codec_layout.addWidget(self.codec_combo)
        settings_layout.addLayout(codec_layout)

        # Bitrate mode
        bitrate_mode_layout = QHBoxLayout()
        bitrate_mode_layout.addWidget(QLabel("Bitrate Mode:"))
        self.bitrate_mode_combo = QComboBox()
        self.bitrate_mode_combo.addItems(["cbr", "vbr"])
        bitrate_mode_layout.addWidget(self.bitrate_mode_combo)
        settings_layout.addLayout(bitrate_mode_layout)

        # Bitrate
        bitrate_layout = QHBoxLayout()
        bitrate_layout.addWidget(QLabel("Bitrate (kbps):"))
        self.bitrate_spin = QSpinBox()
        self.bitrate_spin.setRange(100, 100000)
        bitrate_layout.addWidget(self.bitrate_spin)
        settings_layout.addLayout(bitrate_layout)

        # Audio source
        audio_layout = QHBoxLayout()
        audio_layout.addWidget(QLabel("Audio Source:"))
        self.audio_combo = QComboBox()
        self.audio_combo.addItems(["none", "system", "mic", "both"])
        audio_layout.addWidget(self.audio_combo)
        settings_layout.addLayout(audio_layout)

        # Minimize to tray
        self.tray_check = QCheckBox("Minimize to tray while recording")
        settings_layout.addWidget(self.tray_check)

        # Save settings button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        settings_layout.addWidget(save_button)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon())  # Default icon
        self.tray_icon.setToolTip("DualScreen Recorder")

        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        stop_action = QAction("Stop Recording", self)
        stop_action.triggered.connect(self.stop_recording)
        tray_menu.addAction(stop_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def get_default_output(self):
        folder = self.settings.get("output_folder")
        return os.path.join(folder, "recording.mp4")

    def select_output(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Recording", self.get_default_output(), "MP4 files (*.mp4)")
        if file_path:
            self.output_edit.setText(file_path)
            self.settings.set("output_folder", os.path.dirname(file_path))

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        output_file = self.output_edit.text()
        if not output_file:
            QMessageBox.warning(self, "Error", "Please select an output file.")
            return

        self.recorder.start_recording(output_file)
        self.is_recording = True
        self.record_button.setText("Stop Recording")
        self.status_label.setText("Recording...")
        self.tabs.setEnabled(False)

        if self.tray_check.isChecked():
            self.hide()
            self.tray_icon.showMessage("Recording Started", "Screen recording is in progress.", QSystemTrayIcon.Information)

    def stop_recording(self):
        self.recorder.stop_recording()
        self.is_recording = False
        self.record_button.setText("Start Recording")
        self.status_label.setText("Ready")
        self.tabs.setEnabled(True)
        self.show()

    def load_settings(self):
        self.fps_spin.setValue(self.settings.get("fps"))
        self.codec_combo.setCurrentText(self.settings.get("codec"))
        self.bitrate_mode_combo.setCurrentText(self.settings.get("bitrate_mode"))
        self.bitrate_spin.setValue(self.settings.get("bitrate"))
        self.audio_combo.setCurrentText(self.settings.get("audio_source"))
        self.tray_check.setChecked(self.settings.get("minimize_to_tray"))

    def save_settings(self):
        self.settings.set("fps", self.fps_spin.value())
        self.settings.set("codec", self.codec_combo.currentText())
        self.settings.set("bitrate_mode", self.bitrate_mode_combo.currentText())
        self.settings.set("bitrate", self.bitrate_spin.value())
        self.settings.set("audio_source", self.audio_combo.currentText())
        self.settings.set("minimize_to_tray", self.tray_check.isChecked())
        QMessageBox.information(self, "Settings", "Settings saved.")

    def closeEvent(self, event):
        if self.is_recording:
            self.stop_recording()
        event.accept()