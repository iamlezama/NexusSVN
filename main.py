import tkinter as tk
from src.app import NexusSVNApp

if __name__ == "__main__":
    root = tk.Tk()
    app = NexusSVNApp(root)
    root.mainloop()