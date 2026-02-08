import customtkinter as ctk
import keyboard

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent, settings, on_save_callback):
        super().__init__(parent)
        self.settings = settings
        self.on_save_callback = on_save_callback
        self.recording_hotkey = False
        self.recorded_keys = []  # Initialize here
        self.final_hotkey = None  # Initialize final_hotkey
        
        self.title("⚙️ Settings")
        self.geometry("500x500")  # Increased height
        
        # Colors
        self.colors = {
            "bg": "#0f0f23",
            "card": "#1a1a2e",
            "accent": "#a855f7",
            "text": "#ffffff",
            "text_secondary": "#94a3b8"
        }
        
        self.configure(fg_color=self.colors["bg"])
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.create_ui()
        
    def create_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=self.colors["text"]
        )
        header.pack(pady=20)
        
        # Scrollable settings container
        scroll_container = ctk.CTkScrollableFrame(
            self, 
            fg_color=self.colors["card"], 
            corner_radius=12,
            height=320  # Increased height
        )
        scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Hotkey setting
        hotkey_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        hotkey_frame.pack(fill="x", padx=20, pady=15)
        
        hotkey_label = ctk.CTkLabel(
            hotkey_frame,
            text="🔑 Toggle Hotkey",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        hotkey_label.pack(anchor="w", pady=(0, 5))
        
        hotkey_desc = ctk.CTkLabel(
            hotkey_frame,
            text="Press the button and type your desired hotkey combination",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_secondary"]
        )
        hotkey_desc.pack(anchor="w", pady=(0, 10))
        
        self.hotkey_button = ctk.CTkButton(
            hotkey_frame,
            text=self.settings.get('hotkey', 'shift+e').upper(),
            command=self.record_hotkey,
            fg_color=self.colors["accent"],
            hover_color="#9333ea",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=40,
            width=200
        )
        self.hotkey_button.pack(anchor="w")
        
        # Key mode selection (NEW)
        keymode_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        keymode_frame.pack(fill="x", padx=20, pady=15)
        
        keymode_label = ctk.CTkLabel(
            keymode_frame,
            text="⌨️ Key Mode",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        keymode_label.pack(anchor="w", pady=(0, 5))
        
        keymode_desc = ctk.CTkLabel(
            keymode_frame,
            text="Choose which keys to use for emoji input",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_secondary"]
        )
        keymode_desc.pack(anchor="w", pady=(0, 10))
        
        key_modes = ["Numpad Only", "Top Row Only", "Both (Numpad + Top Row)"]
        current_mode = self.settings.get('key_mode', 'Both (Numpad + Top Row)')
        
        self.keymode_var = ctk.StringVar(value=current_mode)
        self.keymode_menu = ctk.CTkOptionMenu(
            keymode_frame,
            values=key_modes,
            variable=self.keymode_var,
            fg_color=self.colors["accent"],
            button_color="#9333ea",
            button_hover_color="#7e22ce",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            width=250
        )
        self.keymode_menu.pack(anchor="w")
        
        # Discord mode
        discord_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        discord_frame.pack(fill="x", padx=20, pady=15)
        
        discord_label = ctk.CTkLabel(
            discord_frame,
            text="💬 Discord Optimization",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        discord_label.pack(anchor="w", pady=(0, 5))
        
        discord_desc = ctk.CTkLabel(
            discord_frame,
            text="Optimized emoji injection for Discord (faster, clipboard restore)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_secondary"]
        )
        discord_desc.pack(anchor="w", pady=(0, 10))
        
        self.discord_switch = ctk.CTkSwitch(
            discord_frame,
            text="Enable Discord Mode",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors["text"],
            fg_color=self.colors["accent"],
            progress_color=self.colors["accent"]
        )
        if self.settings.get('discord_mode', True):
            self.discord_switch.select()
        self.discord_switch.pack(anchor="w")
        
        # Injection speed
        speed_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        speed_frame.pack(fill="x", padx=20, pady=15)
        
        speed_label = ctk.CTkLabel(
            speed_frame,
            text="⚡ Injection Speed",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["text"]
        )
        speed_label.pack(anchor="w", pady=(0, 5))
        
        speed_desc = ctk.CTkLabel(
            speed_frame,
            text="Lower delay = faster (may cause issues in some apps)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_secondary"]
        )
        speed_desc.pack(anchor="w", pady=(0, 10))
        
        speed_options = ["Ultra Fast (5ms)", "Fast (10ms)", "Normal (20ms)", "Safe (50ms)"]
        speed_values = [0.005, 0.01, 0.02, 0.05]
        current_delay = self.settings.get('injection_delay', 0.02)
        
        # Find closest option
        current_index = min(range(len(speed_values)), key=lambda i: abs(speed_values[i] - current_delay))
        
        self.speed_var = ctk.StringVar(value=speed_options[current_index])
        self.speed_values_map = dict(zip(speed_options, speed_values))
        
        self.speed_menu = ctk.CTkOptionMenu(
            speed_frame,
            values=speed_options,
            variable=self.speed_var,
            fg_color=self.colors["accent"],
            button_color="#9333ea",
            button_hover_color="#7e22ce",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            width=200
        )
        self.speed_menu.pack(anchor="w")
        
        # Buttons - OUTSIDE scrollable container so they're always visible
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save",
            command=self.save_settings,
            fg_color=self.colors["accent"],
            hover_color="#9333ea",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=40,
            width=120
        )
        save_btn.pack(side="right", padx=5)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="#64748b",
            hover_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=40,
            width=120
        )
        cancel_btn.pack(side="right", padx=5)
        
        reset_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Reset",
            command=self.reset_settings,
            fg_color="#ef4444",
            hover_color="#dc2626",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=40,
            width=120
        )
        reset_btn.pack(side="left", padx=5)
    
    def record_hotkey(self):
        """Record a new hotkey without freezing UI"""
        if self.recording_hotkey:
            return
        
        self.recording_hotkey = True
        self.recorded_keys = []
        self.hotkey_button.configure(text="Press keys...", fg_color="#ef4444")
        
        # Simple approach: record all keys pressed
        pressed_keys = set()
        
        def on_key(event):
            if event.event_type == 'down' and event.name not in pressed_keys:
                pressed_keys.add(event.name)
                # Update display
                combo = '+'.join(sorted(pressed_keys))
                self.hotkey_button.configure(text=combo.upper())
            elif event.event_type == 'up' and len(pressed_keys) > 0:
                # User released a key - save the combination
                self.final_hotkey = '+'.join(sorted(pressed_keys))
                print(f"Recorded hotkey: {self.final_hotkey}")  # Debug
                keyboard.unhook_all()
                self.recording_hotkey = False
                self.hotkey_button.configure(fg_color=self.colors["accent"])
        
        # Hook all keyboard events
        keyboard.hook(on_key, suppress=False)
    
    def save_settings(self):
        """Save settings and close"""
        # Get hotkey - use the recorded one if available
        if hasattr(self, 'final_hotkey') and self.final_hotkey:
            print(f"Saving hotkey: {self.final_hotkey}")  # Debug
            self.settings.set('hotkey', self.final_hotkey)
        else:
            print("No new hotkey recorded")  # Debug
        
        # Get key mode
        key_mode = self.keymode_var.get()
        print(f"Saving key mode: {key_mode}")  # Debug
        self.settings.set('key_mode', key_mode)
        
        # Get Discord mode
        discord_mode = self.discord_switch.get() == 1
        print(f"Saving Discord mode: {discord_mode}")  # Debug
        self.settings.set('discord_mode', discord_mode)
        
        # Get injection speed
        speed_text = self.speed_var.get()
        delay = self.speed_values_map.get(speed_text, 0.02)
        print(f"Saving injection delay: {delay}")  # Debug
        self.settings.set('injection_delay', delay)
        
        print("Settings saved successfully!")  # Debug
        
        # Call callback
        if self.on_save_callback:
            self.on_save_callback()
        
        self.destroy()
    
    def reset_settings(self):
        """Reset to defaults"""
        self.settings.reset()
        
        # Update UI
        self.hotkey_button.configure(text=self.settings.get('hotkey', 'shift+e').upper())
        
        if self.settings.get('discord_mode', True):
            self.discord_switch.select()
        else:
            self.discord_switch.deselect()
        
        self.speed_var.set("Normal (20ms)")
