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
    