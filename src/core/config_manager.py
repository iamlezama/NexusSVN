import json
import os
from tkinter import messagebox

class ConfigManager:
    def __init__(self):
        self.appdata_dir = os.path.join(os.getenv('APPDATA'), 'NexusSVN')
        os.makedirs(self.appdata_dir, exist_ok=True)
        self.config_file = os.path.join(self.appdata_dir, 'config.json')
        self.config = {}
        self.load_config()
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "working_copies_dir": "",
                    "repo_url": "",
                    "path_segment": ""
                }
                self.save_config()
        except json.JSONDecodeError:
            messagebox.showerror("Config Error", f"Error reading {self.config_file}. It might be corrupted. Resetting to default.")
            self.config = {
                "working_copies_dir": "",
                "repo_url": "",
                "path_segment": ""
            }
            self.save_config()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred loading config: {e}")
            self.config = {
                "working_copies_dir": "",
                "repo_url": "",
                "path_segment": ""
            }
            self.save_config()
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save configuration: {e}")
    def get(self, key, default=None):
        return self.config.get(key, default)
    def set(self, key, value):
        self.config[key] = value
        self.save_config()