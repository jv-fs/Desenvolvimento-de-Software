import tkinter as tk
from tkinter import filedialog

ERROR_DISPLAY_DURATION = 3000


class ActionsController:
    def __init__(self, gui, callback_commander):
        self.gui = gui

        self.on_load_callback = callback_commander.get("load_data")
        self.get_text_callback = callback_commander.get("getText")
        self.has_error_callback = callback_commander.get("has_error")
        self.play_midi_callback = callback_commander.get("play_midi")

    def handle_file_open(self):
        path = filedialog.askopenfilename(parent=self.gui.root)

        if not path:
            return

        self.on_load_callback(path)

        error = self.has_error_callback()

        if error:
            self.gui.error_label.config(text=error)

            self.gui.root.after(
                ERROR_DISPLAY_DURATION,
                lambda: self.gui.error_label.config(text="")
            )

            return

        content = "\n".join(self.get_text_callback())

        self.gui.text_area.delete("1.0", tk.END)
        self.gui.text_area.insert("1.0", content)
        self.gui._update_voices_number_from_board()

    def handle_play(self):
        self.play_midi_callback()