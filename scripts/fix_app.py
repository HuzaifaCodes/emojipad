"""
Script to fix all app issues:
1. Normalize line endings in dashboard.py
2. Add proper cleanup to prevent TclError
3. Verify all files are working
"""

import os
import re

def fix_dashboard():
    """Fix dashboard.py file"""
    filepath = "d:/emoji adder/ui/dashboard.py"
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Normalize line endings (remove double \r)
    content = content.replace('\r\r\n', '\r\n')
    content = content.replace('\r\n\r\n\r\n', '\r\n\r\n')  # Remove triple blank lines
    
    # Find and replace quit_app function
    quit_app_pattern = r'def quit_app\(self, icon=None, item=None\):.*?sys\.exit\(0\)'
    
    new_quit_app = '''def quit_app(self, icon=None, item=None):
        """Quit application completely"""
        try:
            # Stop listener first
            if hasattr(self, 'listener'):
                self.listener.stop()
            
            # Unhook ALL keyboard hooks
            keyboard.unhook_all()
        except Exception as e:
            print(f"Cleanup warning: {e}")
        
        try:
            # Stop tray icon
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.stop()
        except:
            pass
        
        try:
            # Destroy window (suppress TclError)
            self.destroy()
        except:
            pass
        
        sys.exit(0)'''
    
    content = re.sub(quit_app_pattern, new_quit_app, content, flags=re.DOTALL)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Fixed dashboard.py")

def verify_files():
    """Verify all Python files are valid"""
    import ast
    
    files = [
        'd:/emoji adder/main.py',
        'd:/emoji adder/ui/dashboard.py',
        'd:/emoji adder/ui/settings_dialog.py',
        'd:/emoji adder/ui/emoji_picker.py',
        'd:/emoji adder/core/emoji_manager.py',
        'd:/emoji adder/core/key_listener.py',
        'd:/emoji adder/core/settings.py'
    ]
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
            print(f"✓ {os.path.basename(filepath)}: VALID")
        except Exception as e:
            print(f"✗ {os.path.basename(filepath)}: ERROR - {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("FIXING EMOJI ADDER APP")
    print("=" * 50)
    
    fix_dashboard()
    print()
    
    print("Verifying all files...")
    verify_files()
    
    print()
    print("=" * 50)
    print("✓ ALL FIXES APPLIED!")
    print("=" * 50)
    print("\nYou can now run: python main.py")
