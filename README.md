<div align="center">

# ✨ EmojiPad

### Transform Your Numpad Into an Emoji Powerhouse

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**EmojiPad** is a sleek Windows application that transforms your numeric keypad into a customizable emoji launcher. Express yourself faster with one-key emoji insertion! 🚀

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Building](#-building-from-source) • [Contributing](#-contributing)

</div>

---

## 🎯 Features

### Core Functionality
- **🎨 Customizable Emoji Mapping** - Assign any emoji to any numpad key
- **🔄 Multiple Preset Modes** - Switch between Smileys, Travel, Food, Custom, and more
- **⚡ Global Hotkey** - Toggle emoji mode with `Shift+E` from anywhere
- **🔍 Smart Emoji Picker** - Search through 1000+ emojis with instant filtering
- **📌 Recent Emojis** - Quick access to your frequently used emojis

### User Experience
- **🌙 Modern Dark UI** - Beautiful gradient interface with smooth animations
- **🎭 System Tray Integration** - Runs quietly in the background
- **🚀 Startup Support** - Launch automatically with Windows (optional)
- **💾 Auto-Save** - Your mappings are saved automatically
- **⚙️ Customizable Settings** - Adjust hotkeys and preferences

### Technical Highlights
- **🪶 Lightweight** - Minimal resource usage
- **🔒 Secure** - No internet connection required
- **📦 Portable** - Single executable, no installation needed
- **🎯 Non-Intrusive** - Works alongside your normal numpad usage

---

## 📸 Screenshots

### Main Dashboard
*The main dashboard showing the numpad grid with emoji mappings in Smileys mode*

![Dashboard](https://via.placeholder.com/800x600/1a1a2e/eee?text=EmojiPad+Dashboard)

### Emoji Picker
*Search and select from 1000+ emojis organized by category*

![Emoji Picker](https://via.placeholder.com/600x500/16213e/eee?text=Emoji+Picker+Dialog)

### System Tray
*Convenient system tray menu for quick access*

![System Tray](https://via.placeholder.com/300x200/0f3460/eee?text=System+Tray+Menu)

---

## 🚀 Installation

### Option 1: Download Installer (Recommended)
1. Download the latest `EmojiPad_Setup.exe` from [Releases](https://github.com/HuzaifaCodes/emojipad/releases)
2. Run the installer
3. Choose installation options:
   - ✅ Create desktop shortcut
   - ✅ Run at Windows startup
4. Launch EmojiPad from Start Menu or Desktop

### Option 2: Portable Executable
1. Download `EmojiPad.exe` from [Releases](https://github.com/HuzaifaCodes/emojipad/releases)
2. Place it in any folder
3. Run `EmojiPad.exe`
4. No installation required!

---

## 💡 Usage

### Getting Started
1. **Launch EmojiPad** - Open from Start Menu, Desktop, or System Tray
2. **Choose a Mode** - Select from Smileys, Travel, Food, or Custom
3. **Customize Mappings** - Click any numpad key to assign a new emoji
4. **Toggle Emoji Mode** - Press `Shift+E` to enable/disable emoji insertion

### How It Works
1. Press `Shift+E` to activate emoji mode (status shown in system tray)
2. Press any numpad key (0-9, +, -, *, /, .) to insert the mapped emoji
3. The emoji is automatically typed at your cursor position
4. Press `Shift+E` again to return to normal numpad mode

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Shift+E` | Toggle emoji mode on/off |
| `Numpad 0-9` | Insert mapped emoji (when active) |
| `Numpad +, -, *, /` | Insert mapped emoji (when active) |

### Tips & Tricks
- **Quick Access**: Right-click the system tray icon for instant controls
- **Recent Emojis**: Your last used emojis appear at the top of the picker
- **Custom Mode**: Create your own personalized emoji set
- **Minimize to Tray**: Close the window to run in background

---

## 🛠️ Building from Source

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) Inno Setup for creating installer

### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/HuzaifaCodes/emojipad.git
cd emojipad

# Install dependencies
pip install -r requirements.txt
```

### Run from Source
```bash
python main.py
```

### Build Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller EmojiPad.spec

# Output: dist/EmojiPad.exe
```

### Create Installer
```bash
# Install Inno Setup from https://jrsoftware.org/isdl.php

# Compile installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

# Output: installer_output/EmojiPad_Setup.exe
```

For detailed build instructions, see [BUILD.md](BUILD.md)

---

## 📁 Project Structure

```
emojipad/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── EmojiPad.spec          # PyInstaller configuration
├── installer.iss          # Inno Setup script
├── icon.ico               # Application icon
├── emoji_data.json        # Emoji database
├── core/                  # Core functionality
│   ├── emoji_manager.py   # Emoji mapping logic
│   ├── key_listener.py    # Keyboard hook handler
│   └── settings.py        # Settings management
├── ui/                    # User interface
│   ├── dashboard.py       # Main window
│   ├── emoji_picker.py    # Emoji selection dialog
│   └── settings_dialog.py # Settings window
└── dist/                  # Build output
    └── EmojiPad.exe       # Compiled executable
```

---

## 🎨 Customization

### Adding Custom Emoji Modes
Edit `emoji_data.json` to add new preset modes:
```json
{
  "modes": {
    "YourMode": {
      "0": "🎯",
      "1": "🚀",
      ...
    }
  }
}
```

### Changing Hotkeys
Open Settings dialog in the app or edit `settings.json`:
```json
{
  "toggle_hotkey": "shift+e",
  "startup_enabled": true
}
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Ideas for Contributions
- 🌍 Add support for more emoji categories
- 🎨 Create new UI themes
- 🔧 Improve performance
- 📝 Enhance documentation
- 🐛 Fix bugs

---

## 📋 Requirements

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8+ (for development)
- **RAM**: 50MB minimum
- **Disk**: 20MB

### Python Dependencies
- `customtkinter` - Modern UI framework
- `keyboard` - Global keyboard hooks
- `emoji` - Emoji data and utilities
- `pyperclip` - Clipboard operations
- `pillow` - Image processing
- `pystray` - System tray integration

---

## 🐛 Troubleshooting

### Emoji mode not activating?
- Ensure the app is running (check system tray)
- Try changing the hotkey in Settings
- Run as Administrator if needed

### Emojis not inserting?
- Make sure emoji mode is ON (check tray icon)
- Verify NumLock is enabled
- Check if the target app supports Unicode

### App not starting?
- Install Visual C++ Redistributable
- Check Windows Event Viewer for errors
- Run from command line to see error messages

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **CustomTkinter** - For the beautiful modern UI framework
- **Python Community** - For amazing libraries and support
- **Emoji Contributors** - For maintaining emoji standards

---

## 📞 Contact

**Huzaifa** - [@HuzaifaCodes](https://github.com/HuzaifaCodes)

Project Link: [https://github.com/HuzaifaCodes/emojipad](https://github.com/HuzaifaCodes/emojipad)

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

Made with ❤️ and ☕ by [Huzaifa](https://github.com/HuzaifaCodes)

</div>
