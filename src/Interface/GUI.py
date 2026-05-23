import tkinter as tk
from tkinter import filedialog, ttk
from src.Interface.Modules.Buttons import Buttons
from src.Interface.Modules.GIFPlayer import GIFPlayer

ERROR_DISPLAY_DURATION = 3000  # Duration to display error messages in milliseconds

class GUI:
    def __init__(self, actions_controller):
        
        self.actions_controller = actions_controller

        self.selected_voice_index = None
        self.voices_number = 0

        self.requires_compile = False
        self.transient_error_message = ""
        
        self.root = tk.Tk()
        self.root.title("MIDI Converter")

        self.instruments = self._create_instrument_map()

        self._build_layout()
        self._create_binds()

        self._update_interface()


    ##############################################
    #       Basic GUI setup and layout methods:
    ##############################################
    def _build_layout(self):

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=20)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, padx=20)

        self.gif_player = GIFPlayer(self.main_frame,"assets/rick-astley.gif")

        self.side_buttons = Buttons(self.right_frame)
      
        self.bottom_buttons_frame = tk.Frame(self.root)
        self.bottom_buttons_frame.pack(pady=10)

        self.player_buttons = Buttons(self.bottom_buttons_frame)

        self._create_error_label()
        self._create_voice_selector()
        self._create_instrument_selector()
        self._create_text_area()
       
        self.side_buttons.create_file_button()
        
        self.player_buttons.create_compile_button()    
        self.player_buttons.create_play_button()
        self.player_buttons.create_stop_button()
        self.player_buttons.create_restart_button()
        self.player_buttons.create_loop_button()

    def _create_binds(self):
        self.root.bind("<<play>>", lambda e: self._react_to_play_button_click())
        self.root.bind("<<stop>>", lambda e: self._react_to_stop_button_click())
        self.root.bind("<<restart>>", lambda e: self._react_to_restart_button_click())
        self.root.bind("<<loop>>", lambda e: self._react_to_loop_button_click())
        self.root.bind("<<file_open>>", lambda e: self._react_to_file_open_button_click())
        self.root.bind("<<compile>>", lambda e: self._react_to_compile_button_click())
    
    def _react_to_play_button_click(self):

        if self.requires_compile:
                self._refresh_error_label()
                return

        if not self._has_text_content():
            return

        self.gif_player.start()
        self.actions_controller.trigger_play()

    def _react_to_stop_button_click(self):
        self.actions_controller.trigger_stop()
    
    def _react_to_restart_button_click(self):

        if self.requires_compile:
                self._refresh_error_label()
                return  

        if not self._has_text_content():
            return

        self.gif_player.start()
        self.actions_controller.trigger_restart()
    
    def _react_to_loop_button_click(self):
        self.actions_controller.trigger_loop()
    
    def _react_to_file_open_button_click(self):
        self._handle_file_open()
        
    def _react_to_compile_button_click(self):
        self.actions_controller.trigger_stop()
        self._handle_compile()

    def _update_interface(self):
        is_playing = self.actions_controller.trigger_get_is_playing()
        self.player_buttons.update_play_button(is_playing)

        is_loop_enabled = self.actions_controller.trigger_get_is_loop_enabled()
        self.player_buttons.update_loop_button(is_loop_enabled)

        self.player_buttons.update_compile_button(self.requires_compile)
        self._refresh_error_label()

        if not is_playing:
            self.gif_player.stop()

        self.root.after(100, self._update_interface)


    def _create_error_label(self):
        self.error_label = tk.Label(self.root, text="", fg="red", font=("Arial", 10, "bold"))
        self.error_label.pack(pady=(0, 5))

    def _create_voice_selector(self):
        frame = tk.Frame(self.left_frame)
        frame.pack(pady=10)

        tk.Label(frame, text="Selecionar Voz:").pack(side=tk.LEFT, padx=5)

        self.voice_combobox = ttk.Combobox(frame, state="readonly", width=15)
        self.voice_combobox.pack(side=tk.LEFT, padx=5)

        self.voice_combobox.bind("<<ComboboxSelected>>", self._handle_voice_change)
        self._refresh_voice_selector()

    def _create_instrument_selector(self):
        frame = tk.Frame(self.left_frame)
        frame.pack(pady=10)

        tk.Label(frame, text="Instrumento:").pack(side=tk.LEFT, padx=5)

        options = list(self.instruments.keys())
        self.instrument_combobox = ttk.Combobox(frame, values=options, state="readonly", width=20)
        self.instrument_combobox.pack(side=tk.LEFT, padx=5)

        self.instrument_combobox.bind("<<ComboboxSelected>>", self._handle_instrument_change)

        self._sync_instrument_with_voice()

    def _create_text_area(self):
        tk.Label(self.right_frame, text="Digite a codificação da sua música:").pack()

        self.text_area = tk.Text(self.right_frame, height=10, width=40)
        self.text_area.pack(pady=10)
        self.text_area.bind("<KeyRelease>", self._handle_text_change)

    ##############################################
    #              Handlers:
    ##############################################
    
    def _handle_text_change(self, event=None):

        self.requires_compile = True
        self._refresh_error_label()

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
        self.transient_error_message = message
        self._refresh_error_label()
        self.root.after(ERROR_DISPLAY_DURATION, self._clear_transient_error_message)

    def _clear_transient_error_message(self):
        self.transient_error_message = ""
        self._refresh_error_label()

    def _refresh_error_label(self):
        messages = []

        if self.requires_compile:
            messages.append("Compile novamente antes de tocar.")

        if self.transient_error_message:
            messages.append(self.transient_error_message)

        self.error_label.config(text="\n".join(messages))

    def _has_text_content(self):
        return bool(self.text_area.get("1.0", tk.END).strip())

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

        self.requires_compile = True
        self._refresh_error_label()


    def _handle_compile(self):
        self.actions_controller.trigger_set_text(self.text_area.get("1.0", tk.END))
        self.actions_controller.trigger_compile()

        self.requires_compile = False
        self._refresh_error_label()

    ##############################################
    # Public methods to interact with the GUI:
    ##############################################

    def run(self):
        self.root.mainloop()