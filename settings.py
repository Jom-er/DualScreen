import json
import os

class Settings:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.defaults = {
            "fps": 30,
            "codec": "h264",
            "bitrate_mode": "vbr",
            "bitrate": 5000,  # kbps
            "audio_source": "system",  # system, mic, both
            "output_folder": os.path.expanduser("~/Videos"),
            "minimize_to_tray": True,
            "video_quality": 80,  # for vbr
        }
        self.settings = self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return {**self.defaults, **json.load(f)}
            except:
                pass
        return self.defaults.copy()

    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save()