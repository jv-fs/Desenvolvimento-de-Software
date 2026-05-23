import tkinter as tk

HORIZONTAL_PADDING = 5
VERTICAL_PADDING = 10


class Buttons:
    def __init__(self, root):
        self.root = root

        self.play_button = None
        self.loop_button = None
        self.compile_button = None

    def _create_button(self, text, event, bg=None, fg=None):
        button = tk.Button(
            self.root,
            text=text,
            bg=bg,
            fg=fg,
            command=lambda: self.root.event_generate(event)
        )
        button.pack(side=tk.LEFT, padx=HORIZONTAL_PADDING, pady=VERTICAL_PADDING)
        return button

    def create_play_button(self):
        self.play_button = self._create_button("Play", "<<play>>", bg="green", fg="white")

    def create_stop_button(self):
        self._create_button("Stop", "<<stop>>", bg="red", fg="white")
    
    def create_restart_button(self):
        self._create_button("Restart", "<<restart>>", bg="orange", fg="black")

    def create_loop_button(self):
        self.loop_button = self._create_button("Loop", "<<loop>>", bg="blue", fg="white")

    def create_file_button(self):
        self._create_button("Abrir Arquivo de Texto", "<<file_open>>", bg="gray", fg="white")

    def create_compile_button(self):
        self.compile_button = self._create_button("Compilar", "<<compile>>", bg="purple", fg="white")

    def create_save_button(self):
        self._create_button("Salvar MIDI", "<<save_file>>", bg="brown", fg="white")

    def update_play_button(self, is_playing):
        if self.play_button:
            if is_playing:
                self.play_button.config(bg="black")
            else:
                self.play_button.config(bg="green")
    
    def update_loop_button(self, is_loop_enabled):
        if self.loop_button:
            if is_loop_enabled:
                self.loop_button.config(bg="black")
            else:
                self.loop_button.config(bg="blue")

    def update_compile_button(self, requires_compile):
        if self.compile_button:
            if requires_compile:
                self.compile_button.config(bg="red")
            else:
                self.compile_button.config(bg="purple")