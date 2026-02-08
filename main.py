from ui.dashboard import DashboardApp
import sys
import os

# Ensure we can find the core/ui modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    app = DashboardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()