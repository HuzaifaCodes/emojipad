import json
import os

class Settings:
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = {
            "hotkey": "shift+e",
            "key_mode": "Both (Numpad + Top Row)",
            "injection_method": "paste",  # paste or type
            "injection_delay": 0.02,
            "discord_mode": True,  # Optimized for Discord
            "startup": False
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create default"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.default_settings, **loaded}
            except:
                return self.default_settings.copy()
        return self.default_settings.copy()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def reset(self):
        """Reset to default settings"""
        self.settings = self.default_settings.copy()
        self.save_settings()
