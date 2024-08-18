import tkinter as tk
from app import CheatSheetApp
from screeninfo import get_monitors

def main():
    root = tk.Tk()
    secondary_root = tk.Toplevel()

    monitors = get_monitors()
    if len(monitors) > 1:
        second_monitor = monitors[1]
        secondary_root.geometry(f"{second_monitor.width}x{second_monitor.height}+{second_monitor.x}+{second_monitor.y}")
    else:
        secondary_root.geometry("800x450")

    app = CheatSheetApp(root, secondary_root)
    root.mainloop()

if __name__ == "__main__":
    main()
