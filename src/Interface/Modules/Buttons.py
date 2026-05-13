import tkinter as tk

class Buttons:
    def __init__(self, root):
        self.root = root
    
    def create_play_button(self):
        tk.Button(
            self.root,
            text="Play",
            command= lambda: self.root.event_generate("<<play>>")
        ).pack(pady=10)

    def create_file_button(self):
        tk.Button(
            self.root,
            text="Abrir Arquivo de Texto",
            command= lambda: self.root.event_generate("<<file_open>>")
        ).pack(pady=10)

    def create_compile_button(self):
        tk.Button(
            self.root,
            text="Compilar",
            command= lambda: self.root.event_generate("<<compile>>")
        ).pack(pady=10)
    