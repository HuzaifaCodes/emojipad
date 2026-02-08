import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkfont
import emoji as emoji_lib
import json
import os

class EmojiPickerDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.selected_emoji = None
        self.recent_file = "recent_emojis.json"
        self.recent_emojis = self.load_recent_emojis()
        
        self.title("Emoji Picker")
        self.geometry("500x600")
        
        # Windows emoji picker inspired colors
        self.colors = {
            "bg": "#f3f3f3",
            "search_bg": "#ffffff",
            "category_bg": "#ffffff",
            "hover": "#e5e5e5",
            "selected": "#0078d4",
            "text": "#1f1f1f",
            "text_secondary": "#605e5c",
            "border": "#d1d1d1"
        }
        
        self.configure(fg_color=self.colors["bg"])
        
        # Popular emojis categorized (Windows style categories)
        self.emoji_categories = {
            "😀 Smileys": ["😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂", "🙃", "😉", "😊", "😇", "🥰", "😍", "🤩", "😘", "😗", "😚", "😙", "🥲", "☺️", "😌", "😏", "😴", "😪", "🤤", "😋", "😛", "😜", "🤪", "😝", "🤑", "🤗", "🤭", "🤫", "🤔", "🤐", "🤨", "😐", "😑", "😶", "😒", "🙄", "😬", "🤥", "😔", "😷", "🤒", "🤕", "🤢", "🤮", "🤧", "🥵", "🥶", "😵", "🤯", "🤠", "🥳", "😎", "🤓", "🧐", "😕", "😟", "🙁", "☹️", "😮", "😯", "😲", "😳", "🥺", "😦", "😧", "😨", "😰", "😥", "😢", "😭", "😱", "😖", "😣", "😞", "😓", "😩", "😫", "🥱", "😤", "😡", "😠", "🤬", "💀", "☠️", "💩", "🤡", "👹", "👺", "👻", "👽", "👾", "🤖"],
            "👋 People": ["👋", "🤚", "🖐️", "✋", "🖖", "👌", "🤌", "🤏", "✌️", "🤞", "🤟", "🤘", "🤙", "👈", "👉", "👆", "🖕", "👇", "☝️", "👍", "👎", "✊", "👊", "🤛", "🤜", "👏", "🙌", "👐", "🤲", "🤝", "🙏", "✍️", "💅", "🤳", "💪", "🦾", "🦿", "🦵", "🦶", "👂", "🦻", "👃", "🧠", "🫀", "🫁", "🦷", "🦴", "👀", "👁️", "👅", "👄", "💋", "🩸"],
            "❤️ Hearts": ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❤️‍🔥", "❤️‍🩹", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟", "☮️", "✝️", "☪️", "🕉️", "☸️", "✡️", "🔯", "🕎", "☯️", "☦️", "🛐", "⛎", "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"],
            "🐶 Animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐽", "🐸", "🐵", "🙈", "🙉", "🙊", "🐔", "🐧", "🐦", "🐤", "🐣", "🐥", "🦆", "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🪱", "🐛", "🦋", "🐌", "🐞", "🐜", "🪰", "🪲", "🪳", "🦟", "🦗", "🕷️", "🕸️", "🦂", "🐢", "🐍", "🦎", "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🦣", "🐘", "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🐃", "🐂", "🐄", "🐎", "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🐈", "🐓", "🦃", "🦚", "🦜", "🦢", "🦩", "🕊️", "🐇", "🦝", "🦨", "🦡", "🦫", "🦦", "🦥", "🐁", "🐀", "🐿️", "🦔"],
            "🍕 Food": ["🍕", "🍔", "🍟", "🌭", "🍿", "🧈", "🍖", "🍗", "🥓", "🥚", "🍳", "🧇", "🥞", "🍞", "🥐", "🥨", "🥯", "🥖", "🧀", "🥗", "🥙", "🌮", "🌯", "🥪", "🍱", "🍛", "🍜", "🍝", "🍠", "🍢", "🍣", "🍤", "🍥", "🥮", "🍡", "🥟", "🥠", "🥡", "🦀", "🦞", "🦐", "🦑", "🦪", "🍦", "🍧", "🍨", "🍩", "🍪", "🎂", "🍰", "🧁", "🥧", "🍫", "🍬", "🍭", "🍮", "🍯", "🍼", "🥛", "☕", "🫖", "🍵", "🍶", "🍾", "🍷", "🍸", "🍹", "🍺", "🍻", "🥂", "🥃", "🥤", "🧋", "🧃", "🧉", "🧊"],
            "⚽ Activities": ["⚽", "🏀", "🏈", "⚾", "🥎", "🎾", "🏐", "🏉", "🥏", "🎱", "🏓", "🏸", "🏒", "🏑", "🥍", "🏏", "🥅", "⛳", "🏹", "🎣", "🤿", "🥊", "🥋", "🎽", "🛹", "🛼", "🛷", "⛸️", "🥌", "🎿", "⛷️", "🏂", "🪂", "🏋️", "🤼", "🤸", "🤺", "⛹️", "🤾", "🏌️", "🏇", "🧘", "🏊", "🤽", "🚣", "🧗", "🚴", "🚵", "🎪", "🎭", "🎨", "🎬", "🎤", "🎧", "🎼", "🎹", "🥁", "🪘", "🎷", "🎺", "🪗", "🎸", "🪕", "🎻", "🎲", "♟️", "🎯", "🎳", "🎮", "🎰", "🧩"],
            "✈️ Travel": ["🚗", "🚕", "🚙", "🚌", "🚎", "🏎️", "🚓", "🚑", "🚒", "🚐", "🛻", "🚚", "🚛", "🚜", "🦯", "🦽", "🦼", "🛴", "🚲", "🛵", "🏍️", "🛺", "🚨", "🚔", "🚍", "🚘", "🚖", "🚡", "🚠", "🚟", "🚃", "🚋", "🚞", "🚝", "🚄", "🚅", "🚈", "🚂", "🚆", "🚇", "🚊", "🚉", "✈️", "🛫", "🛬", "🛩️", "💺", "🛰️", "🚀", "🛸", "🚁", "🛶", "⛵", "🚤", "🛥️", "🛳️", "⛴️", "🚢", "⚓", "⛽", "🚧", "🚦", "🚥", "🚏", "🗺️", "🗿", "🗽", "🗼", "🏰", "🏯", "🏟️", "🎡", "🎢", "🎠", "⛲", "⛱️", "🏖️", "🏝️"],
            "💡 Objects": ["⌚", "📱", "💻", "⌨️", "🖥️", "🖨️", "🖱️", "🖲️", "🕹️", "🗜️", "💾", "💿", "📀", "📼", "📷", "📸", "📹", "🎥", "📞", "☎️", "📟", "📠", "📺", "📻", "🎙️", "🎚️", "🎛️", "🧭", "⏱️", "⏲️", "⏰", "🕰️", "⌛", "⏳", "📡", "🔋", "🔌", "💡", "🔦", "🕯️", "🪔", "🧯", "🛢️", "💸", "💵", "💴", "💶", "💷", "🪙", "💰", "💳", "💎", "⚖️", "🪜", "🧰", "🪛", "🔧", "🔨", "⚒️", "🛠️", "⛏️", "🪚", "🔩", "⚙️", "🪤", "🧱", "⛓️", "🧲", "🔫", "💣", "🧨", "🪓", "🔪", "🗡️", "⚔️", "🛡️"],
            "🎉 Symbols": ["❤️", "💯", "✨", "⭐", "🌟", "💫", "🔥", "💥", "💢", "💦", "💨", "🕳️", "💬", "🗨️", "🗯️", "💭", "💤", "🚫", "✅", "❌", "⭕", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "⚪", "🟤", "🔺", "🔻", "🔸", "🔹", "🔶", "🔷", "🔳", "🔲", "▪️", "▫️", "◾", "◽", "◼️", "◻️", "🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "⬛", "⬜", "🟫"]
        }
        
        self.current_category = list(self.emoji_categories.keys())[0]
        
        self.create_ui()
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Keyboard shortcuts
        self.bind("<Escape>", lambda e: self.destroy())
        self.search_entry.bind("<Return>", self.on_search_enter)
        
    def load_recent_emojis(self):
        """Load recently used emojis"""
        if os.path.exists(self.recent_file):
            try:
                with open(self.recent_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_recent_emoji(self, emoji_char):
        """Save emoji to recent list"""
        if emoji_char in self.recent_emojis:
            self.recent_emojis.remove(emoji_char)
        self.recent_emojis.insert(0, emoji_char)
        self.recent_emojis = self.recent_emojis[:18]  # Keep only 18 recent
        
        try:
            with open(self.recent_file, 'w', encoding='utf-8') as f:
                json.dump(self.recent_emojis, f, ensure_ascii=False)
        except:
            pass
        
    def create_ui(self):
        # Search bar (Windows style)
        self.search_frame = ctk.CTkFrame(self, fg_color=self.colors["bg"], corner_radius=0)
        self.search_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Search emojis (press Enter)",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            fg_color=self.colors["search_bg"],
            border_color=self.colors["border"],
            border_width=1,
            corner_radius=4,
            height=36,
            text_color=self.colors["text"]
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self.on_search)
        self.search_entry.focus()
        
        # Recently used section (if any)
        if self.recent_emojis:
            recent_label = ctk.CTkLabel(
                self,
                text="⏱️ Recently Used",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                text_color=self.colors["text_secondary"],
                anchor="w"
            )
            recent_label.pack(fill="x", padx=20, pady=(5, 5))
            
            recent_frame = tk.Frame(self, bg=self.colors["bg"])
            recent_frame.pack(fill="x", padx=20, pady=(0, 10))
            
            for idx, emoji_char in enumerate(self.recent_emojis[:9]):
                btn = tk.Button(
                    recent_frame,
                    text=emoji_char,
                    font=("Segoe UI Emoji", 28),
                    width=2,
                    height=1,
                    bg=self.colors["category_bg"],
                    fg=self.colors["text"],
                    relief="flat",
                    cursor="hand2",
                    command=lambda e=emoji_char: self.select_emoji(e)
                )
                btn.grid(row=0, column=idx, padx=3, pady=2)
                
                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors["hover"]))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors["category_bg"]))
        
        # Category buttons (horizontal scrollable)
        self.category_frame = ctk.CTkFrame(self, fg_color=self.colors["bg"], corner_radius=0, height=50)
        self.category_frame.pack(fill="x", padx=15, pady=(5, 10))
        self.category_frame.pack_propagate(False)
        
        # Scrollable category container
        self.category_scroll = ctk.CTkScrollableFrame(
            self.category_frame,
            fg_color=self.colors["bg"],
            corner_radius=0,
            orientation="horizontal",
            height=40
        )
        self.category_scroll.pack(fill="both", expand=True)
        
        self.category_buttons = {}
        for idx, category in enumerate(self.emoji_categories.keys()):
            btn = ctk.CTkButton(
                self.category_scroll,
                text=category.split()[0],  # Just the emoji icon
                width=45,
                height=40,
                font=ctk.CTkFont(size=20),
                fg_color="transparent",
                hover_color=self.colors["hover"],
                text_color=self.colors["text"],
                corner_radius=4,
                command=lambda c=category: self.select_category(c)
            )
            btn.pack(side="left", padx=2)
            self.category_buttons[category] = btn
        
        # Highlight first category
        self.category_buttons[self.current_category].configure(
            fg_color=self.colors["selected"],
            text_color="white"
        )
        
        # Emoji grid container - use native Tkinter Canvas for better emoji rendering
        self.emoji_container = tk.Frame(self, bg=self.colors["category_bg"], highlightthickness=1, highlightbackground=self.colors["border"])
        self.emoji_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Canvas with scrollbar
        self.canvas = tk.Canvas(self.emoji_container, bg=self.colors["category_bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.emoji_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["category_bg"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling - bind to canvas instead of bind_all
        def on_mousewheel(event):
            if self.canvas.winfo_exists():
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", on_mousewheel)
        
        # Cleanup on destroy
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.display_emojis()
    
    def on_close(self):
        """Clean up before closing"""
        try:
            self.canvas.unbind("<MouseWheel>")
            self.scrollable_frame.unbind("<MouseWheel>")
        except:
            pass
        self.destroy()
        
    def select_category(self, category):
        # Update button styles
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(fg_color=self.colors["selected"], text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=self.colors["text"])
        
        self.current_category = category
        self.display_emojis()
    
    def display_emojis(self):
        # Clear existing
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        emojis = self.emoji_categories[self.current_category]
        
        # Create grid - optimized for performance
        for idx, emoji_char in enumerate(emojis):
            row = idx // 7  # 7 columns for better fit
            col = idx % 7
            
            # Use native Tkinter Button for proper emoji rendering
            btn = tk.Button(
                self.scrollable_frame,
                text=emoji_char,
                font=("Segoe UI Emoji", 30),  # Slightly smaller for performance
                width=2,
                height=1,
                bg=self.colors["category_bg"],
                fg=self.colors["text"],
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda e=emoji_char: self.select_emoji(e)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Simple hover effect (more performant)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors["hover"]))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors["category_bg"]))
    
    def on_search(self, event):
        search_text = self.search_entry.get().lower().strip()
        
        if not search_text:
            self.display_emojis()
            return
        
        # Clear existing
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        matches = []
        for category, emojis in self.emoji_categories.items():
            for emoji_char in emojis:
                # Simple text matching
                if search_text in emoji_char:
                    matches.append(emoji_char)
                    continue
                
                # Try emoji name matching
                try:
                    emoji_name = emoji_lib.demojize(emoji_char).replace('_', ' ').replace(':', '').lower()
                    if search_text in emoji_name:
                        matches.append(emoji_char)
                except:
                    pass
        
        # Display matches
        if not matches:
            no_result = tk.Label(
                self.scrollable_frame,
                text=f"No emojis found for '{search_text}'",
                font=("Segoe UI", 13),
                fg=self.colors["text_secondary"],
                bg=self.colors["category_bg"]
            )
            no_result.grid(row=0, column=0, columnspan=8, pady=50)
        else:
            for idx, emoji_char in enumerate(matches[:64]):  # Limit results
                row = idx // 8
                col = idx % 8
                
                btn = tk.Button(
                    self.scrollable_frame,
                    text=emoji_char,
                    font=("Segoe UI Emoji", 32),
                    width=2,
                    height=1,
                    bg=self.colors["category_bg"],
                    fg=self.colors["text"],
                    relief="flat",
                    cursor="hand2",
                    command=lambda e=emoji_char: self.select_emoji(e)
                )
                btn.grid(row=row, column=col, padx=3, pady=3)
                
                # Hover effect
                def on_enter(event, b=btn):
                    b.configure(bg=self.colors["selected"], relief="raised")
                
                def on_leave(event, b=btn):
                    b.configure(bg=self.colors["category_bg"], relief="flat")
                
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
    
    def on_search_enter(self, event):
        """Select first emoji when Enter is pressed in search"""
        search_text = self.search_entry.get().lower().strip()
        if not search_text:
            return
        
        # Find first match
        for category, emojis in self.emoji_categories.items():
            for emoji_char in emojis:
                if search_text in emoji_char:
                    self.select_emoji(emoji_char)
                    return
                
                try:
                    emoji_name = emoji_lib.demojize(emoji_char).replace('_', ' ').replace(':', '').lower()
                    if search_text in emoji_name:
                        self.select_emoji(emoji_char)
                        return
                except:
                    pass
    
    def select_emoji(self, emoji_char):
        self.selected_emoji = emoji_char
        self.save_recent_emoji(emoji_char)
        self.callback(emoji_char)
        self.on_close()
