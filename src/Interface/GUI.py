import tkinter as tk
from tkinter import filedialog, ttk
from src.Interface.Modules.Buttons import Buttons

ERROR_DISPLAY_DURATION = 3000  # Duration to display error messages in milliseconds

class GUI:
    def __init__(self, actions_controller):
        
        self.actions_controller = actions_controller

        self.selected_voice_index = None
        self.voices_number = 0
        
        self.root = tk.Tk()
        self.root.title("MIDI Converter")

        self.instruments = self._create_instrument_map()

        self._build_layout()
        self._create_binds()


    ##############################################
    #       Basic GUI setup and layout methods:
    ##############################################

    def _build_layout(self):
        
        self.buttons = Buttons(self.root)
        
        self.buttons.create_file_button()
        self._create_error_label()
        self._create_voice_selector()
        self._create_instrument_selector()
        self.buttons.create_compile_button()
        self._create_text_area()

        self.buttons.create_play_button()
    
    def _create_binds(self):
        self.root.bind("<<play>>", lambda e: self._react_to_play_button_click())
        self.root.bind("<<file_open>>", lambda e: self._react_to_file_open_button_click())
        self.root.bind("<<compile>>", lambda e: self._react_to_compile_button_click())
    
    def _react_to_play_button_click(self):
        self.actions_controller.trigger_play()
    
    def _react_to_file_open_button_click(self):
        self._handle_file_open()
        
    def _react_to_compile_button_click(self):
        self._handle_compile()

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

    ##############################################
    #              Handlers:
    ##############################################
    
    def _handle_text_change(self, event=None):
        self.actions_controller.trigger_set_text(self.text_area.get("1.0", tk.END))
        self._update_voices_number_from_board()

    def _get_instrument_name_from_value(self, instrument_value):
        for name, value in self.instruments.items():
            if value == instrument_value:
                return name

        return None

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

    def _show_error(self, message):
        self.error_label.config(text=message)
        self.root.after(ERROR_DISPLAY_DURATION, lambda: self.error_label.config(text=""))

    def _load_text_to_area(self):
        content = "\n".join(self.actions_controller.trigger_get_text())

        self.text_area.delete("1.0", tk.END) # Clear existing content before inserting new text
        self.text_area.insert("1.0", content)
    

    def _update_voices_number_from_board(self):
        content = self.text_area.get("1.0", tk.END)
        lines = [line for line in content.splitlines() if line.strip()]

        if not lines:
            self.voices_number = 0
            return
        else:
            self.voices_number = len(lines)
   
        self._refresh_voice_selector()

    def _refresh_voice_selector(self): # VERIFICAR
        if self.voices_number == 0:
            self.voice_combobox.config(values=[])
            self.voice_combobox.config(state="disabled")
            
            self.selected_voice_index = None
        else:
            self.voice_combobox.config(state="normal")
            options = [str(i + 1) for i in range(self.voices_number)]
            self.voice_combobox.config(values=options)
    
    def _handle_voice_change(self, event=None):
        self.selected_voice_index = self.voice_combobox.current()
        self._sync_instrument_with_voice()
    
    def _sync_instrument_with_voice(self):
        voice = self.actions_controller.trigger_get_current_voice(self.selected_voice_index)

        if voice:
            instrument_value = voice.getInitialInstrument()

            instrument_name = self._get_instrument_name_from_value(instrument_value)

            if instrument_name:
                self.instrument_combobox.set(instrument_name)
            else:
                self.instrument_combobox.set("Instrumento Desconhecido")
        else:
            self.instrument_combobox.set("")
        
    def _handle_instrument_change(self, event=None):
        selected_instrument = self.instrument_combobox.get()
        if selected_instrument in self.instruments:
            instrument_value = self.instruments[selected_instrument]
            voice = self.actions_controller.trigger_get_current_voice(self.selected_voice_index)
            if voice:
                voice.setInitialInstrument(instrument_value) # <--- Verificar se isso fere algo
    
    def _handle_file_open(self):
        path = filedialog.askopenfilename(parent=self.root)

        if not path:
            return

        self.actions_controller.trigger_load_data(path)

        error = self.actions_controller.trigger_has_error()

        if error:
            self._show_error(error)
            return

        self._load_text_to_area()
        self._update_voices_number_from_board()


    def _handle_compile(self):
        self.actions_controller.trigger_set_text(self.text_area.get("1.0", tk.END))
        self.actions_controller.trigger_compile()

    ##############################################
    # Public methods to interact with the GUI:
    ##############################################

    def run(self):
        self.root.mainloop()