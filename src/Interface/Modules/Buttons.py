import tkinter as tk

class Buttons:
    def __init__(self, root):
        self.root = root

    def _create_button(self, text, event, bg=None, fg=None):
        tk.Button(
            self.root,
            text=text,
            bg=bg,
            fg=fg,
            command=lambda: self.root.event_generate(event)
        ).pack(pady=10)

    def create_play_button(self):
        self._create_button("Play", "<<play>>", bg="green", fg="white")

    def create_stop_button(self):
        self._create_button("Stop", "<<stop>>", bg="red", fg="white")
    
    def create_restart_button(self):
        self._create_button("Restart", "<<restart>>", bg="orange", fg="black")

    def create_loop_button(self):
        self._create_button("Loop", "<<loop>>", bg="blue", fg="white")

    def create_file_button(self):
        self._create_button("Abrir Arquivo de Texto", "<<file_open>>", bg="gray", fg="white")

    def create_compile_button(self):
        self._create_button("Compilar", "<<compile>>", bg="purple", fg="white")
    