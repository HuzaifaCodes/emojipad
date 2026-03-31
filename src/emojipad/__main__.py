from emojipad.ui.dashboard import DashboardApp
import sys
import os

def main():
    app = DashboardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()