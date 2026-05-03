import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class GUI:
    def __init__(self, on_load_callback, text_operator, voices=None):
        self.on_load_callback = on_load_callback
        self.text_operator = text_operator
        self.voices = voices or []
        self.selected_voice_index = 0
        self.root = tk.Tk() # Initialize the main window
        self.root.title("MIDI Converter") # Set the window title
        self._setup_widgets() # Set up the widgets (buttons, etc.) in the GUI

    def _setup_widgets(self):
        # Button to open file dialog for loading text data:
        tk.Button(self.root, text="Abrir Arquivo de Texto", command=self._open_filedialog).pack()

        # Label for error messages (initially hidden)
        self.error_label = tk.Label(self.root, text="", fg="red", font=("Arial", 10, "bold"))
        self.error_label.pack(pady=(0, 5))

        # Frame para Voice selection
        voice_frame = tk.Frame(self.root)
        voice_frame.pack(pady=10)
        
        tk.Label(voice_frame, text="Selecionar Voz:").pack(side=tk.LEFT, padx=5)
        
        voice_options = [f"{i+1}" for i in range(len(self.voices))]
        self.voice_combobox = ttk.Combobox(voice_frame, values=voice_options, state="readonly", width=15)
        self.voice_combobox.pack(side=tk.LEFT, padx=5)
        self.voice_combobox.current(0)
        self.voice_combobox.bind("<<ComboboxSelected>>", self._on_voice_selected)
        
        # Frame para Instrument selection
        instrument_frame = tk.Frame(self.root)
        instrument_frame.pack(pady=10)
        
        tk.Label(instrument_frame, text="Instrumento:").pack(side=tk.LEFT, padx=5)
        
        self.instruments = {
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
        
        instrument_options = list(self.instruments.keys())
        self.instrument_combobox = ttk.Combobox(instrument_frame, values=instrument_options, state="readonly", width=20)
        self.instrument_combobox.pack(side=tk.LEFT, padx=5)
        self.instrument_combobox.bind("<<ComboboxSelected>>", self._on_instrument_changed)
        self._update_instrument_display()

        # Placeholder for text area where the user can input text directly:
        tk.Label(self.root, text="Digite a codificação da sua música no campo a seguir:").pack()
        self.text_area = tk.Text(self.root, height=10, width=40)
        self.text_area.pack(pady=10)

    def _open_filedialog(self):

        path = filedialog.askopenfilename(parent=self.root) # Open file dialog and get the selected path
        if path:
            self.on_load_callback(path)
           
            if self.text_operator.has_error():
                # Mostra mensagem de erro em vermelho
                self.error_label.config(text=self.text_operator.error_message)
                # Remove a mensagem após 3 segundos
                self.root.after(3000, lambda: self.error_label.config(text=""))
            elif hasattr(self.text_operator, 'voices_text') and self.text_operator.voices_text:
                content = '\n'.join(self.text_operator.voices_text)
                self.text_area.delete('1.0', tk.END)  
                self.text_area.insert('1.0', content)
    
    def _on_voice_selected(self, event=None):
        """Callback quando uma voz é selecionada no combobox"""
        self.selected_voice_index = self.voice_combobox.current()
        self._update_instrument_display()
    
    def _update_instrument_display(self):
        """Atualiza o display do instrumento baseado na voz selecionada"""
        if self.selected_voice_index < len(self.voices):
            current_instrument = self.voices[self.selected_voice_index].instrument
            # Encontra o nome do instrumento pelo valor
            for name, value in self.instruments.items():
                if value == current_instrument:
                    self.instrument_combobox.set(name)
                    break
    
    def _on_instrument_changed(self, event=None):
        """Callback quando o instrumento é alterado"""
        if self.selected_voice_index < len(self.voices):
            selected_instrument_name = self.instrument_combobox.get()
            new_instrument_value = self.instruments[selected_instrument_name]
            self.voices[self.selected_voice_index].instrument = new_instrument_value
            print(f"Instrumento da Voz {self.selected_voice_index + 1} alterado para {selected_instrument_name} ({new_instrument_value})") 

    def run(self):
        self.root.mainloop()