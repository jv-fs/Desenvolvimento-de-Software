import tkinter as tk
from tkinter import filedialog, messagebox

class GUI:
    def __init__(self, on_load_callback):
        self.on_load_callback = on_load_callback
        self.root = tk.Tk() # Initialize the main window
        self.root.title("MIDI Converter") # Set the window title
        self._setup_widgets() # Set up the widgets (buttons, etc.) in the GUI

    def _setup_widgets(self):
        # Button to open file dialog for loading text data:
        tk.Button(self.root, text="Abrir Arquivo de Texto", command=self._open_filedialog).pack()

        # Placeholder for text area where the user can input text directly:
        tk.Label(self.root, text="Digite a codificação da sua música no campo a seguir:").pack()
        self.text_area = tk.Text(self.root, height=10, width=40)
        self.text_area.pack(pady=10)


    def _open_filedialog(self):
        path = filedialog.askopenfilename(parent=self.root) # Open file dialog and get the selected path
        if path:
            self.on_load_callback(path, True) # Passes the path to the callback function / True is indicating that it's a path

    def run(self):
        self.root.mainloop()