import tkinter as tk
from tkinter import filedialog, ttk

from src.Utils.VoiceFactory import VoiceFactory


class GUI:
    def __init__(self, callback_commander, voices=None):
        self.on_load_callback = callback_commander.get("load_data")
        self.getText_callback = callback_commander.get("getText")
        self.has_error_callback = callback_commander.get("has_error")
        self.voices = voices or [VoiceFactory.create_voice(text="1", instrument=0, volume=100, tonality="C")]

        self.selected_voice_index = 0
        self.root = tk.Tk()
        self.root.title("MIDI Converter")

        self.instruments = self._create_instrument_map()

        self._build_layout()


    def _build_layout(self):
        self._create_file_button()
        self._create_error_label()
        self._create_voice_selector()
        self._create_instrument_selector()
        self._create_text_area()

    def _create_file_button(self):
        tk.Button(self.root, text="Abrir Arquivo de Texto", command=self._handle_file_open).pack()

    def _create_error_label(self):
        self.error_label = tk.Label(self.root, text="", fg="red", font=("Arial", 10, "bold"))
        self.error_label.pack(pady=(0, 5))

    def _create_voice_selector(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Selecionar Voz:").pack(side=tk.LEFT, padx=5)

        self.voice_combobox = ttk.Combobox(frame, state="readonly", width=15)
        self.voice_combobox.pack(side=tk.LEFT, padx=5)

        self.voice_combobox.bind("<<ComboboxSelected>>", self._handle_voice_change)
        self._refresh_voice_selector()

    def _create_instrument_selector(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Instrumento:").pack(side=tk.LEFT, padx=5)

        options = list(self.instruments.keys())
        self.instrument_combobox = ttk.Combobox(frame, values=options, state="readonly", width=20)
        self.instrument_combobox.pack(side=tk.LEFT, padx=5)

        self.instrument_combobox.bind("<<ComboboxSelected>>", self._handle_instrument_change)

        self._sync_instrument_with_voice()

    def _create_text_area(self):
        tk.Label(self.root, text="Digite a codificação da sua música:").pack()

        self.text_area = tk.Text(self.root, height=10, width=40)
        self.text_area.pack(pady=10)
        self.text_area.bind("<KeyRelease>", self._handle_text_change)

    def _create_instrument_map(self):
        return {
            "Piano": 0,
            "Chromatic Percussion": 1,
            "Harpsichord": 6,
            "Acoustic Guitar": 24,
            "Bass": 33,
            "Strings": 48,
            "Trumpet": 56,
            "Flute": 73,
            "Harmonica": 72
        }

    def _handle_file_open(self):
        path = filedialog.askopenfilename(parent=self.root)
        if not path:
            return

        self.on_load_callback(path)

        error = self.has_error_callback()
        if error:
            self._show_error(error)
            return

        self._load_text_to_area()
        self._update_voices_from_board()

    def _load_text_to_area(self):
        content = "\n".join(self.getText_callback())
        self._set_text(content)

    def _handle_text_change(self, event=None):
        self._update_voices_from_board()

    def _update_voices_from_board(self):
        lines = self._extract_lines_from_board()
        voice_count = len(lines)
        existing_voices = self.voices[:voice_count]

        for i in range(len(existing_voices), voice_count):
            existing_voices.append(
                VoiceFactory.create_voice(
                    text=lines[i],
                    instrument=0,
                    volume=100,
                    tonality="C"
                )
            )

        for i, voice in enumerate(existing_voices):
            voice.text = lines[i]

        self.voices = existing_voices
        self._refresh_voice_selector()

    def _extract_lines_from_board(self):
        content = self.text_area.get("1.0", tk.END)
        lines = [line for line in content.splitlines() if line.strip()]
        if not lines:
            lines = [""]
        return lines

    def _refresh_voice_selector(self):
        self._ensure_at_least_one_voice()
        options = [str(i + 1) for i in range(len(self.voices))]
        self.voice_combobox.config(values=options)

        if options:
            current = self.voice_combobox.current()
            if current < 0 or current >= len(options):
                self.voice_combobox.current(0)

    def _ensure_at_least_one_voice(self):
        if not self.voices:
            self.voices = [VoiceFactory.create_voice(text="1", instrument=0, volume=100, tonality="C")]

    def _set_text(self, content):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", content)

    def _show_error(self, message):
        self.error_label.config(text=message)
        self.root.after(3000, lambda: self.error_label.config(text=""))


    def _handle_voice_change(self, event=None):
        self.selected_voice_index = self.voice_combobox.current()
        self._sync_instrument_with_voice()

    def _get_selected_voice(self):
        if self.selected_voice_index < len(self.voices):
            return self.voices[self.selected_voice_index]
        return None


    def _handle_instrument_change(self, event=None):
        voice = self._get_selected_voice()
        if not voice:
            return

        name = self.instrument_combobox.get()
        voice.instrument = self.instruments[name]

        print(f"Voz {self.selected_voice_index + 1} -> {name}")

    def _sync_instrument_with_voice(self):
        voice = self._get_selected_voice()
        if not voice:
            return

        for name, value in self.instruments.items():
            if value == voice.instrument:
                self.instrument_combobox.set(name)
                break


    def run(self):
        self.root.mainloop()