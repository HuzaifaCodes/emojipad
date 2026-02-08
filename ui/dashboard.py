import customtkinter as ctk
from core.emoji_manager import EmojiManager
from core.key_listener import KeyListener
from core.settings import Settings
from ui.emoji_picker import EmojiPickerDialog
from ui.settings_dialog import SettingsDialog
import threading
import keyboard
import pystray
from PIL import Image, ImageDraw
import sys
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("✨ Emoji Numpad Mapper")
        self.geometry("800x600")
        
        # Modern color palette with gradients
        self.colors = {
            "bg_primary": "#0a0a1a",
            "bg_secondary": "#1a1a2e",
            "bg_tertiary": "#252538",
            "bg_card": "#1e1e30",
            
            "accent_purple": "#a855f7",
            "accent_pink": "#ec4899",
            "accent_blue": "#3b82f6",
            "accent_cyan": "#06b6d4",
            "accent_green": "#10b981",
            
            "text_primary": "#ffffff",
            "text_secondary": "#a0a0b8",
            "text_tertiary": "#6b6b7f",
            
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            
            # Gradient colors for buttons
            "gradient_purple_start": "#667eea",
            "gradient_purple_end": "#764ba2",
            "gradient_pink_start": "#f093fb",
            "gradient_pink_end": "#f5576c",
        }
        
        self.configure(fg_color=self.colors["bg_primary"])
        
        # Initialize components
        self.settings = Settings()
        self.manager = EmojiManager()
        self.listener = KeyListener(self.manager, self.settings)
        self.emoji_mode_enabled = True  # Track if emoji mode is active
        self.tray_icon = None
        self.current_hotkey = None
        
        # Start listener automatically
        self.listener_thread = threading.Thread(target=self.listener.start, daemon=True)
        self.listener_thread.start()
        
        # Setup global hotkey for toggle
        self.setup_toggle_hotkey()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_content()
        
        # Setup system tray
        self.setup_system_tray()
        
        # Handle window close properly
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_toggle_hotkey(self):
        """Setup customizable hotkey to toggle emoji mode"""
        try:
            hotkey = self.settings.get('hotkey', 'shift+e')
            print(f"Setting up hotkey: {hotkey}")  # Debug
            
            # Remove only the previous toggle hotkey if it exists
            if hasattr(self, 'current_hotkey') and self.current_hotkey is not None:
                try:
                    keyboard.remove_hotkey(self.current_hotkey)
                except:
                    pass
            
            # Small delay to ensure cleanup
            import time
            time.sleep(0.02)
            
            # Add new hotkey
            self.current_hotkey = keyboard.add_hotkey(hotkey, self.toggle_emoji_mode, suppress=False)
            print(f"✓ Hotkey '{hotkey}' is now active!")  # Debug
        except Exception as e:
            print(f"✗ Could not setup hotkey: {e}")
    
    def setup_system_tray(self):
        """Create system tray icon"""
        def create_icon_image():
            # Create a simple emoji icon
            width = 64
            height = 64
            image = Image.new('RGB', (width, height), color=(168, 85, 247))
            dc = ImageDraw.Draw(image)
            dc.rectangle([16, 16, 48, 48], fill=(236, 72, 153))
            return image
        
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window, default=True),
            pystray.MenuItem("Toggle Emoji Mode", self.toggle_emoji_mode_from_tray),
            pystray.MenuItem("Settings", lambda: self.after(0, self.open_settings)),
            pystray.MenuItem("Quit", self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("emoji_mapper", create_icon_image(), "Emoji Numpad Mapper", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def hide_to_tray(self):
        """Hide window to system tray"""
        self.withdraw()
        if self.tray_icon:
            self.tray_icon.notify("Emoji Mapper is running in the background", "Click the icon to show the window")
    
    def show_window(self, icon=None, item=None):
        """Show window from tray"""
        self.after(0, self.deiconify)
    
    def toggle_emoji_mode_from_tray(self, icon=None, item=None):
        """Toggle emoji mode from tray menu"""
        self.after(0, self.toggle_emoji_mode)
    
    def quit_app(self, icon=None, item=None):
        """Quit application completely - with proper cleanup"""
        try:
            # Stop listener first
            if hasattr(self, 'listener'):
                try:
                    self.listener.stop()
                except:
                    pass
            
            # Unhook ALL keyboard hooks
            try:
                keyboard.unhook_all()
            except:
                pass
        except:
            pass
        
        try:
            # Stop tray icon
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.stop()
        except:
            pass
        
        try:
            # Destroy window - suppress TclError
            self.destroy()
        except:
            pass
        
        # Force exit
        os._exit(0)
    
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=self.colors["bg_secondary"])
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_propagate(False)
        
        # Logo/Title
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=25)
        
        title = ctk.CTkLabel(
            title_frame,
            text="✨ Emoji\nMapper",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=self.colors["accent_purple"]
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Numpad Edition",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_tertiary"]
        )
        subtitle.pack(pady=(5, 0))
        
        # Mode selector
        mode_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        mode_frame.pack(fill="x", padx=15, pady=15)
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="Quick Mode",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.colors["text_secondary"]
        )
        mode_label.pack(anchor="w", pady=(0, 10), padx=5)
        
        self.mode_var = ctk.StringVar(value="custom")
        
        # Modes with emoji icons
        modes = [
            ("🎨 Custom", "custom"),
            ("😊 Smileys", "smileys"),
            ("🐾 Animals", "animals"),
            ("🍕 Food", "food"),
            ("✈️ Travel", "travel"),
            ("🎯 Objects", "objects")
        ]
        
        for mode_name, mode_value in modes:
            btn = ctk.CTkRadioButton(
                mode_frame,
                text=mode_name,
                variable=self.mode_var,
                value=mode_value,
                command=lambda: self.change_mode(self.mode_var.get()),
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=self.colors["text_primary"],
                fg_color=self.colors["accent_purple"],
                hover_color=self.colors["accent_pink"]
            )
            btn.pack(anchor="w", pady=5, padx=5)
        
        # Spacer
        ctk.CTkLabel(self.sidebar, text="", height=10).pack()
        
        # Toggle button
        hotkey_text = self.settings.get('hotkey', 'shift+e').upper()
        self.toggle_btn = ctk.CTkButton(
            self.sidebar,
            text=f"🔄 Toggle ({hotkey_text})",
            command=self.toggle_emoji_mode,
            fg_color=self.colors["accent_purple"],
            hover_color=self.colors["accent_pink"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=42,
            corner_radius=10
        )
        self.toggle_btn.pack(fill="x", padx=15, pady=8)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Settings",
            command=self.open_settings,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["accent_blue"],
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=36,
            corner_radius=8
        )
        settings_btn.pack(fill="x", padx=15, pady=4)
        

        # Status indicator
        self.status_frame = ctk.CTkFrame(
            self.sidebar, 
            fg_color=self.colors["bg_tertiary"],
            corner_radius=8
        )
        self.status_frame.pack(side="bottom", fill="x", padx=15, pady=15)
        
        self.status_indicator = ctk.CTkLabel(
            self.status_frame,
            text="● Active",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.colors["success"]
        )
        self.status_indicator.pack(pady=8)
    
    def create_main_content(self):
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color=self.colors["bg_primary"])
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        
        # Simplified header for better performance
        header = ctk.CTkFrame(
            self.main_content, 
            fg_color=self.colors["bg_secondary"], 
            height=75,
            corner_radius=12
        )
        header.pack(fill="x", padx=20, pady=(20, 15))
        header.pack_propagate(False)
        
        header_title = ctk.CTkLabel(
            header,
            text="Numpad Emoji Mappings",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        header_title.pack(side="left", padx=20)
        
        # Quick actions
        self.quick_actions = ctk.CTkFrame(header, fg_color="transparent")
        self.quick_actions.pack(side="right", padx=15)
        

        self.clear_btn = ctk.CTkButton(
            self.quick_actions,
            text="🗑️ Clear All",
            command=self.clear_all_mappings,
            fg_color=self.colors["danger"],
            hover_color="#dc2626",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            width=100,
            height=34,
            corner_radius=8
        )
        self.clear_btn.pack(side="right", padx=4)
        
        # Grid container
        self.grid_container = ctk.CTkScrollableFrame(
            self.main_content,
            fg_color="transparent"
        )
        self.grid_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.create_numpad_grid()
    
    def create_numpad_grid(self):
        # Clear existing
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        
        # Proper numpad layout (like calculator/phone)
        numpad_keys = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '.', 'enter']
        ]
        
        # Create centered container for keypad
        keypad_container = ctk.CTkFrame(self.grid_container, fg_color="transparent")
        keypad_container.pack(expand=True, pady=40)
        
        for row_idx, row in enumerate(numpad_keys):
            row_frame = ctk.CTkFrame(keypad_container, fg_color="transparent")
            row_frame.pack(pady=4)
            
            for col_idx, key in enumerate(row):
                # Get emoji for this key
                emoji_char = self.manager.get_emoji(key)
                has_emoji = emoji_char is not None
                
                # Keypad-style button card
                key_card = ctk.CTkFrame(
                    row_frame,
                    fg_color=self.colors["bg_card"],
                    corner_radius=10,
                    width=140,
                    height=140
                )
                key_card.pack(side="left", padx=8)
                key_card.pack_propagate(False)
                
                # Small key label at top
                key_label = ctk.CTkLabel(
                    key_card,
                    text=key.upper(),
                    font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
                    text_color=self.colors["text_tertiary"]
                )
                key_label.pack(pady=(8, 0))
                
                # Emoji display area (clickable)
                if has_emoji:
                    # Show emoji directly without button background
                    emoji_display = ctk.CTkLabel(
                        key_card,
                        text=emoji_char,
                        font=ctk.CTkFont(size=48),
                        text_color=self.colors["text_primary"],
                        cursor="hand2"
                    )
                    emoji_display.pack(expand=True)
                    
                    # Make it clickable
                    emoji_display.bind("<Button-1>", lambda e, k=key: self.edit_key(k))
                    
                    # Add hover effect
                    def on_enter(e, lbl=emoji_display):
                        lbl.configure(text_color=self.colors["accent_purple"])
                    
                    def on_leave(e, lbl=emoji_display):
                        lbl.configure(text_color=self.colors["text_primary"])
                    
                    emoji_display.bind("<Enter>", on_enter)
                    emoji_display.bind("<Leave>", on_leave)
                else:
                    # Show + icon to add emoji
                    add_btn = ctk.CTkLabel(
                        key_card,
                        text="➕",
                        font=ctk.CTkFont(size=40),
                        text_color=self.colors["text_tertiary"],
                        cursor="hand2"
                    )
                    add_btn.pack(expand=True)
                    
                    # Make it clickable
                    add_btn.bind("<Button-1>", lambda e, k=key: self.edit_key(k))
                    
                    # Add hover effect
                    def on_enter_add(e, lbl=add_btn):
                        lbl.configure(text_color=self.colors["accent_purple"])
                    
                    def on_leave_add(e, lbl=add_btn):
                        lbl.configure(text_color=self.colors["text_tertiary"])
                    
                    add_btn.bind("<Enter>", on_enter_add)
                    add_btn.bind("<Leave>", on_leave_add)
    
    def get_button_text(self, key):
        return self.manager.get_emoji(key) or "➕"
    
    def change_mode(self, new_mode):
        """Change emoji mode and refresh grid"""
        # Capitalize mode name to match EmojiManager format
        mode_name = new_mode.capitalize()
        self.manager.set_mode(mode_name)
        self.refresh_grid()
        self.show_temp_message(f"Switched to {mode_name} mode")
    
    def animate_mode_change(self):
        # Simple fade effect
        self.refresh_grid()
    
    def refresh_grid(self):
        self.create_numpad_grid()
    
    def edit_key(self, key):
        """Open emoji picker for a specific key"""
        def on_emoji_picked(emoji_char):
            self.manager.set_emoji(key, emoji_char)
            self.refresh_grid()
            self.show_temp_message(f"Mapped {emoji_char} to Numpad {key}")
        
        EmojiPickerDialog(self, on_emoji_picked)
    
    def show_temp_message(self, message):
        # Create temporary message overlay
        msg_label = ctk.CTkLabel(
            self.main_content,
            text=message,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=self.colors["success"],
            corner_radius=8,
            text_color="white"
        )
        msg_label.place(relx=0.5, rely=0.95, anchor="center")
        
        # Auto-hide after 2 seconds
        self.after(2000, msg_label.destroy)
    
    def toggle_emoji_mode(self):
        """Toggle between emoji mode and normal numpad mode"""
        self.emoji_mode_enabled = not self.emoji_mode_enabled
        
        if self.emoji_mode_enabled:
            self.status_indicator.configure(
                text="● Active",
                text_color=self.colors["success"]
            )
            self.show_temp_message("✅ Emoji Mode Enabled")
            # Restart listener
            self.listener.stop()
            import time
            time.sleep(0.1)
            self.listener = KeyListener(self.manager, self.settings)
            self.listener_thread = threading.Thread(target=self.listener.start, daemon=True)
            self.listener_thread.start()
            # Re-register toggle hotkey after listener starts
            time.sleep(0.05)
            self.setup_toggle_hotkey()
        else:
            self.status_indicator.configure(
                text="● Paused",
                text_color=self.colors["warning"]
            )
            self.show_temp_message("⏸️ Emoji Mode Paused")
            self.listener.stop()
            # Re-register toggle hotkey after stopping listener
            import time
            time.sleep(0.05)
            self.setup_toggle_hotkey()
    
    def clear_all_mappings(self):
        """Clear all custom mappings"""
        # Confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Clear")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text="Clear all emoji mappings?",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=30)
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            width=100
        ).pack(side="left", padx=10)
        
        def confirm():
            self.manager.clear_all()
            self.refresh_grid()
            self.show_temp_message("🗑️ All mappings cleared")
            dialog.destroy()
        
        ctk.CTkButton(
            btn_frame,
            text="Clear All",
            command=confirm,
            fg_color=self.colors["danger"],
            width=100
        ).pack(side="left", padx=10)
    
    
    
    def open_settings(self):
        """Open settings dialog"""
        def on_save():
            # Completely reset keyboard hooks
            try:
                keyboard.unhook_all()
                print("Cleared all keyboard hooks")  # Debug
            except:
                pass
            
            # Small delay to ensure hooks are cleared
            import time
            time.sleep(0.1)
            
            # Refresh hotkey with new settings
            self.current_hotkey = None  # Reset
            self.setup_toggle_hotkey()
            
            # Update toggle button text
            hotkey_text = self.settings.get('hotkey', 'shift+e').upper()
            self.toggle_btn.configure(text=f"🔄 Toggle ({hotkey_text})")
            
            # Restart listener to apply key mode changes
            self.listener.stop()
            time.sleep(0.1)
            self.listener = KeyListener(self.manager, self.settings)
            self.listener_thread = threading.Thread(target=self.listener.start, daemon=True)
            self.listener_thread.start()
            
            self.show_temp_message("Settings saved! Hotkey updated.")
        
        SettingsDialog(self, self.settings, on_save)
    
    def on_closing(self):
        """Override to hide to tray instead of closing"""
        self.hide_to_tray()

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
