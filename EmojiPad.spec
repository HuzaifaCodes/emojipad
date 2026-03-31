# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=['src'],
    binaries=[],
    datas=[('icon.ico', '.')],
    hiddenimports=['pystray._win32', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6',  # Exclude Qt frameworks
        'matplotlib', 'numpy', 'pandas', 'scipy',  # Exclude data science libs
        'pytest', 'unittest', 'doctest',  # Exclude test frameworks
        'tkinter.test', 'test',  # Exclude test modules
        '_pytest', 'py.test',
        'IPython', 'jupyter',  # Exclude jupyter
        'setuptools', 'pip', 'wheel',  # Exclude build tools
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EmojiPad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # DISABLED — UPX compression triggers antivirus false positives
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version='version_info.txt',  # Version metadata helps AV trust the exe
)
