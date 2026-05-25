import tkinter as tk

from PIL import Image, ImageTk

FRAME_DELAY = 50
CURRENT_FRAME = 0

class GIFPlayer:

    def __init__(self, parent, gif_path):

        self.parent = parent
        self.gif_path = gif_path
        self.frame_delay = FRAME_DELAY
        self.frames = []
        self.current_frame = CURRENT_FRAME
        self.is_animating = False
        self.is_visible = True

        self._load_frames()

        self.label = tk.Label(self.parent)

        self.label.pack()

    def _load_frames(self):

        gif = Image.open(self.gif_path)

        try:

            while True:

                frame = gif.copy()

                photo_frame = ImageTk.PhotoImage(frame)

                self.frames.append(photo_frame)

                gif.seek(len(self.frames))

        except EOFError:
            pass


    def start(self):

        if self.is_animating:
            return

        self.is_animating = True

        self._animate()
        self._show()

    def stop(self):

        self.is_animating = False
        self._hide()

    def _animate(self):

        if not self.is_animating:
            return

        frame = self.frames[self.current_frame]

        self.label.config(image=frame)

        self.current_frame += 1

        if self.current_frame >= len(self.frames):
            self.current_frame = CURRENT_FRAME

        self.parent.after(
            self.frame_delay,
            self._animate
        )

    def _hide(self):

        if not self.is_visible:
            return

        self.label.pack_forget()

        self.is_visible = False
        
    def _show(self):

        if self.is_visible:
            return

        self.label.pack()

        self.is_visible = True