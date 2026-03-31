# EmojiPad Build Instructions

## Prerequisites
1. Install PyInstaller: `pip install pyinstaller`
2. Download and install [Inno Setup](https://jrsoftware.org/isdl.php)
3. Create an icon file named `icon.ico` (64x64 or 256x256)

## Building the Executable

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Step 2: Build with PyInstaller
```bash
pyinstaller EmojiPad.spec
```

This will create:
- `dist/EmojiPad.exe` - The standalone executable

### Step 3: Create Installer with Inno Setup
1. Open Inno Setup Compiler
2. Open `installer.iss`
3. Click "Build" > "Compile"
4. The installer will be created in `installer_output/EmojiPad_Setup.exe`

## Quick Build Script (PowerShell)
```powershell
# Build executable
pyinstaller EmojiPad.spec

# Compile installer (adjust path to your Inno Setup installation)
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

## Features
- ✅ System tray icon
- ✅ Minimize to tray
- ✅ Run at startup (optional during installation)
- ✅ Tray menu with Show/Toggle/Exit
- ✅ Desktop shortcut (optional)
- ✅ Start menu shortcuts

## Testing
1. Run `dist/EmojiPad.exe` to test the standalone executable
2. Install using `installer_output/EmojiPad_Setup.exe`
3. Check if startup option works (restart Windows)
4. Verify system tray functionality

## Notes
- The app runs in the background when closed (minimizes to tray)
- Use the tray icon to show/hide the dashboard
- Press Shift+E to toggle emoji mode from anywhere
- Uninstall removes startup registry entry automatically
