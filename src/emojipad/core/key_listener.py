import keyboard
import pyperclip
import time
from threading import Thread

class KeyListener:
    def __init__(self, emoji_manager, settings=None):
        self.manager = emoji_manager
        self.settings = settings
        self.running = False
        self.enabled = True  # Can be toggled on/off
        self.hooked_keys = []
        self.clipboard_restore = True  # Restore clipboard after paste

    def start(self):
        self.running = True
        
        # Get key mode preference
        key_mode = "Both (Numpad + Top Row)"
        if self.settings:
            key_mode = self.settings.get('key_mode', 'Both (Numpad + Top Row)')
        
        # Hook specific numpad keys with suppression
        if key_mode in ["Numpad Only", "Both (Numpad + Top Row)"]:
            for i in range(10):
                try:
                    keyboard.hook_key(f'num {i}', self.on_key_event, suppress=True)
                except:
                    pass
        
        # Top row number keys (for laptops)
        if key_mode in ["Top Row Only", "Both (Numpad + Top Row)"]:
            for i in range(10):
                try:
                    keyboard.hook_key(str(i), self.on_key_event, suppress=True)
                except:
                    pass

    def on_key_event(self, event):
        if not self.running or not self.enabled or event.event_type != 'down':
            return True  # Don't suppress if not enabled
        
        # Check if it's a numpad key OR top number row key
        key_name = event.name
        digit = None
        
        # Handle both 'num 0' format and direct numpad scan codes
        if key_name.startswith('num '):
            try:
                digit = key_name.split(' ')[1]
            except:
                return True
        elif len(key_name) == 1 and key_name.isdigit():
            # This could be numpad with numlock OR top number row
            # Numpad scan codes: 82(0), 79(1), 80(2), 81(3), 75(4), 76(5), 77(6), 71(7), 72(8), 73(9)
            # Top row scan codes: 11(0), 2(1), 3(2), 4(3), 5(4), 6(5), 7(6), 8(7), 9(8), 10(9)
            numpad_scancodes = {82: '0', 79: '1', 80: '2', 81: '3', 75: '4', 76: '5', 77: '6', 71: '7', 72: '8', 73: '9'}
            toprow_scancodes = {11: '0', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9'}
            
            if event.scan_code in numpad_scancodes:
                digit = numpad_scancodes[event.scan_code]
            elif event.scan_code in toprow_scancodes:
                # Top number row - also support this for laptops!
                digit = toprow_scancodes[event.scan_code]
        
        if digit is None:
            return True  # Don't suppress unknown keys
        
        # Check if we have a mapping
        emoji_char = self.manager.get_mapping(digit)
        
        if emoji_char:
            # Inject emoji in a separate thread to avoid blocking
            Thread(target=self._inject_async, args=(emoji_char,), daemon=True).start()
            return False  # Suppress the original key event
        else:
            return True  # Allow the number to be typed if no mapping

    def _inject_async(self, emoji_char):
        """Inject emoji asynchronously"""
        # Get delay from settings or use default
        delay = 0.01
        if self.settings:
            delay = self.settings.get('injection_delay', 0.01)
        
        time.sleep(delay)
        self.inject_emoji(emoji_char)
        self.manager.register_usage(emoji_char)

    def inject_emoji(self, char):
        """Optimized emoji injection for Discord and other apps"""
        try:
            # Discord-optimized paste method
            original_clipboard = ""
            
            # Save clipboard only if restore is enabled
            if self.clipboard_restore:
                try:
                    original_clipboard = pyperclip.paste()
                except:
                    pass
            
            # Copy emoji to clipboard
            pyperclip.copy(char)
            
            # Minimal delay for Discord
            time.sleep(0.005)
            
            # Paste using Ctrl+V
            keyboard.press('ctrl')
            keyboard.press('v')
            keyboard.release('v')
            keyboard.release('ctrl')
            
            # Restore clipboard after a short delay
            if self.clipboard_restore and original_clipboard:
                time.sleep(0.02)
                try:
                    pyperclip.copy(original_clipboard)
                except:
                    pass
                    
        except Exception as e:
            print(f"Error injecting emoji: {e}")

    def stop(self):
        self.running = False
        keyboard.unhook_all()
    
    def set_enabled(self, enabled):
        """Enable or disable emoji injection"""
        self.enabled = enabled

