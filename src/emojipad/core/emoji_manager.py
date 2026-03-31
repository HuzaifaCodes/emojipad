import json
import os
from collections import defaultdict
import emoji

DATA_FILE = "emoji_data.json"

class EmojiManager:
    def __init__(self):
        # Mode-specific mappings: {mode_name: {numpad_key: emoji_char}}
        self.mode_mappings = {
            "Custom": {},
            "Smileys": {},
            "Animals": {},
            "Food": {},
            "Travel": {},
            "Objects": {}
        }
        
        # Default emoji profiles (read-only templates)
        self.emotion_profiles = {
            "Smileys": ["😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂"],
            "Animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨"],
            "Food": ["🍕", "🍔", "🍟", "🌭", "🍿", "🧂", "🥓", "🥚", "🍳"],
            "Travel": ["✈️", "🚗", "🚕", "🚙", "🚌", "🚎", "🏎️", "🚓", "🚑"],
            "Objects": ["⌚", "📱", "💻", "⌨️", "🖥️", "🖨️", "🖱️", "🖲️", "🕹️"]
        }
        self.current_mode = "Custom"
        self.usage_history = defaultdict(int)
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Load mode-specific mappings
                    self.mode_mappings = data.get("mode_mappings", self.mode_mappings)
                    self.emotion_profiles.update(data.get("emotion_profiles", {}))
                    self.usage_history = defaultdict(int, data.get("usage_history", {}))
                    self.current_mode = data.get("current_mode", "Custom")
            except Exception as e:
                print(f"Error loading data: {e}")

    def save_data(self):
        data = {
            "mode_mappings": self.mode_mappings,
            "emotion_profiles": self.emotion_profiles,
            "usage_history": self.usage_history,
            "current_mode": self.current_mode
        }
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def get_mapping(self, key):
        """Returns the emoji mapped to the given key (str '0'-'9') based on current mode."""
        # Get mode-specific mappings
        mode_map = self.mode_mappings.get(self.current_mode, {})
        
        # Check if user has set a custom mapping for this key in current mode
        if str(key) in mode_map:
            return mode_map[str(key)]
        
        # Fall back to default profile if no custom mapping
        profile = self.emotion_profiles.get(self.current_mode, [])
        if not profile:
            return None
        
        # Map numpad keys to profile indices
        try:
            idx = int(key)
            list_idx = -1
            if 1 <= idx <= 9:
                list_idx = idx - 1
            elif idx == 0:
                list_idx = 9
            
            if 0 <= list_idx < len(profile):
                return profile[list_idx]
        except ValueError:
            pass
        
        return None

    def set_mapping(self, key, emoji_char):
        """Sets a mapping for the current mode."""
        # Ensure mode exists in mode_mappings
        if self.current_mode not in self.mode_mappings:
            self.mode_mappings[self.current_mode] = {}
        
        # Set the mapping for current mode
        self.mode_mappings[self.current_mode][str(key)] = emoji_char
        self.save_data()
        return True

    def register_usage(self, emoji_char):
        if not emoji_char: return
        self.usage_history[emoji_char] += 1
        self.save_data()

    def set_mode(self, mode):
        if mode in self.emotion_profiles or mode == "Custom":
            self.current_mode = mode
            self.save_data()

    def get_current_mappings(self):
        """Returns a dict of all current mappings {key: emoji} for UI display."""
        result = {}
        for i in range(10):
            mapping = self.get_mapping(str(i))
            if mapping:
                result[str(i)] = mapping
        return result
    
    def get_emoji(self, key):
        """Alias for get_mapping - for backward compatibility"""
        return self.get_mapping(key)
    
    def set_emoji(self, key, emoji_char):
        """Alias for set_mapping - for backward compatibility"""
        return self.set_mapping(key, emoji_char)
    
    def clear_all(self):
        """Clear all emoji mappings for current mode"""
        if self.current_mode in self.mode_mappings:
            self.mode_mappings[self.current_mode] = {}
        self.save_data()
