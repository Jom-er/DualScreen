import cv2
import mss
import numpy as np
import threading
import time
import os
import pyaudio
import wave
import ffmpeg
from settings import Settings

class ScreenRecorder:
    def __init__(self):
        self.settings = Settings()
        self.is_recording = False
        self.video_thread = None
        self.audio_thread = None
        self.temp_video = "temp_video.avi"
        self.temp_audio = "temp_audio.wav"
        self.output_file = None

    def start_recording(self, output_file):
        if self.is_recording:
            return
        self.is_recording = True
        self.output_file = output_file

        # Start video recording
        self.video_thread = threading.Thread(target=self.record_video)
        self.video_thread.start()

        # Start audio recording if needed
        audio_source = self.settings.get("audio_source")
        if audio_source != "none":
            self.audio_thread = threading.Thread(target=self.record_audio)
            self.audio_thread.start()

    def stop_recording(self):
        if not self.is_recording:
            return
        self.is_recording = False

        if self.video_thread:
            self.video_thread.join()
        if self.audio_thread:
            self.audio_thread.join()

        # Combine video and audio if needed
        self.combine_av()

        # Clean up temp files
        if os.path.exists(self.temp_video):
            os.remove(self.temp_video)
        if os.path.exists(self.temp_audio):
            os.remove(self.temp_audio)

    def record_video(self):
        fps = self.settings.get("fps")
        codec = self.settings.get("codec")
        bitrate = self.settings.get("bitrate") * 1000  # kbps to bps

        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            width = monitor["width"]
            height = monitor["height"]

            fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Temp codec
            out = cv2.VideoWriter(self.temp_video, fourcc, fps, (width, height))

            while self.is_recording:
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)
                time.sleep(1 / fps)

            out.release()

    def record_audio(self):
        audio_source = self.settings.get("audio_source")
        # For simplicity, record microphone
        # System audio is harder, requires pulseaudio or something
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 2
        fs = 44100

        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []

        while self.is_recording:
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.temp_audio, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def combine_av(self):
        if not os.path.exists(self.temp_video):
            return

        codec = self.settings.get("codec")
        bitrate = self.settings.get("bitrate")
        bitrate_mode = self.settings.get("bitrate_mode")

        video_input = ffmpeg.input(self.temp_video)
        if os.path.exists(self.temp_audio):
            audio_input = ffmpeg.input(self.temp_audio)
            stream = ffmpeg.concat(video_input, audio_input, v=1, a=1)
        else:
            stream = video_input

        output_args = {
            'vcodec': f'lib{codec}',
            'acodec': 'aac' if os.path.exists(self.temp_audio) else None,
            'audio_bitrate': '128k' if os.path.exists(self.temp_audio) else None
        }

        if bitrate_mode == 'cbr':
            output_args['video_bitrate'] = f'{bitrate}k'
        else:  # vbr
            if codec == 'h264':
                output_args['crf'] = 23  # Default, can adjust based on quality
            elif codec == 'h265':
                output_args['crf'] = 28

        stream = stream.output(self.output_file, **{k: v for k, v in output_args.items() if v is not None})
        stream.run(overwrite_output=True)