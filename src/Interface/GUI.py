import tkinter as tk
from tkinter import filedialog, ttk
from src.Interface.Modules.Buttons import Buttons
from src.Interface.Modules.GIFPlayer import GIFPlayer
from src.Utils.MIDITable import Instruments

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
        self.side_buttons.create_save_text_button()
        self.side_buttons.create_save_button()

        self._create_volume_slider()
        
        self.player_buttons.create_compile_button()    
        self.player_buttons.create_play_button()
        self.player_buttons.create_stop_button()
        self.player_buttons.create_restart_button()
        self.player_buttons.create_loop_button()

    def _create_binds(self): # Determinates the reactions to button clicks by binding custom events to the root window and triggering them in the button command callbacks
        self.root.bind("<<play>>", lambda e: self._react_to_play_button_click())
        self.root.bind("<<stop>>", lambda e: self._react_to_stop_button_click())
        self.root.bind("<<restart>>", lambda e: self._react_to_restart_button_click())
        self.root.bind("<<loop>>", lambda e: self._react_to_loop_button_click())
        self.root.bind("<<file_open>>", lambda e: self._react_to_file_open_button_click())
        self.root.bind("<<save_text_file>>", lambda e: self._react_to_save_text_file_button_click())
        self.root.bind("<<compile>>", lambda e: self._react_to_compile_button_click())
        self.root.bind("<<save_file>>", lambda e: self._react_to_save_file_button_click())
    
    ##############################################
    #            Bind Reactions:
    ##############################################

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

    def _react_to_save_text_file_button_click(self):
        if not self._has_text_content():
            return

        self._handle_save_text_file()

    def _react_to_save_file_button_click(self):
        if self.requires_compile:
                self._refresh_error_label()
                return  

        if not self._has_text_content():
            return
        
        self._handle_save_midi()

    ##############################################
    #            Updater:
    ##############################################

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

        tk.Label(frame, text="Instrumento (0-127):").pack(side=tk.LEFT, padx=5)

        self.instrument_number_var = tk.StringVar()
        self.instrument_number_var.trace_add("write", self._update_instrument_label)

        self.instrument_spinbox = ttk.Spinbox(
            frame, 
            from_=0, 
            to=127, 
            width=5, 
            textvariable=self.instrument_number_var
        )
        self.instrument_spinbox.pack(side=tk.LEFT, padx=5)

        # Dynamical instrument name label
        self.instrument_name_label = tk.Label(frame, text="---")
        self.instrument_name_label.pack(side=tk.LEFT, padx=5)

        self._sync_instrument_with_voice()

    def _create_text_area(self):
        tk.Label(self.right_frame, text="Digite a codificação da sua música:").pack()

        self.text_area = tk.Text(self.right_frame, height=10, width=40)
        self.text_area.pack(pady=10)
        self.text_area.bind("<KeyRelease>", self._handle_text_change)
    
    def _create_volume_slider(self):
        frame = tk.Frame(self.bottom_buttons_frame)
        frame.pack(pady=10)

        tk.Label(frame, text="Volume Global:").pack(side=tk.LEFT, padx=5)

        self.volume_scale = tk.Scale(
            frame,
            from_=0.0,
            to=1.5,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self._handle_volume_change # Método chamado diretamenta pela ausência de um Event Bus (não necesário)
        )

        self.volume_scale.set(1.0)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

    ##############################################
    #              Handlers:
    ##############################################

    def _handle_volume_change(self, value):
        volume_float = float(value)
        
        self.actions_controller.trigger_set_volume(volume_float)
    
    def _handle_text_change(self, event=None):

        self.requires_compile = True
        self._refresh_error_label()

        self.actions_controller.trigger_set_text(self.text_area.get("1.0", tk.END))
        self._update_voices_number_from_board()
    
    def _handle_voice_change(self, event=None):
        self.selected_voice_index = self.voice_combobox.current()
        self._sync_instrument_with_voice()
    
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
        
        self.actions_controller.trigger_prepare_voices()

        memory = getattr(self, 'user_selected_instruments', {})
        for v_index, instr_num in memory.items():
            self.actions_controller.trigger_set_voice_instrument(v_index, instr_num)

        self.actions_controller.trigger_finish_compile()

        self._sync_instrument_with_voice()
        self.requires_compile = False
        self._refresh_error_label()

    def _handle_save_midi(self):
        
        path = filedialog.asksaveasfilename(
        parent=self.root,
        defaultextension=".mid",
        filetypes=[("MIDI files", "*.mid")]
        )

        if not path:
            return

        self.actions_controller.trigger_save_file(path)

        self.requires_compile = False
        self._refresh_error_label()

    def _handle_save_text_file(self):
        path = filedialog.asksaveasfilename(
            parent=self.root,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )

        if not path:
            return

        self.actions_controller.trigger_save_text_file(path)
    
    ##############################################
    #              Labels and text area:
    ##############################################

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
    
    def _update_instrument_label(self, *args):
        entry = self.instrument_number_var.get()
        
        try:
            number = int(entry)

            if 0 <= number <= 127:
                name = Instruments.getInstrumentFromNumber(number)
                self.instrument_name_label.config(text=name)
                
                if self.selected_voice_index is not None and not getattr(self, '_is_syncing_ui', False):
                    
                    if not hasattr(self, 'user_selected_instruments'):
                        self.user_selected_instruments = {}
                    self.user_selected_instruments[self.selected_voice_index] = number
                    
                    self.actions_controller.trigger_set_voice_instrument(self.selected_voice_index, number)
                    
            else:
                self.instrument_name_label.config(text="Fora do limite")
                
        except ValueError:
            self.instrument_name_label.config(text="Inválido")
    
    ##############################################
    #            Voices and Instruments:
    ##############################################

    def _update_voices_number_from_board(self):
        content = self.text_area.get("1.0", tk.END)
        lines = [line for line in content.splitlines() if line.strip()]

        if not lines:
            self.voices_number = 0
            return
        else:
            self.voices_number = len(lines)
   
        self._refresh_voice_selector()

    def _refresh_voice_selector(self):
        if self.voices_number == 0:
            self.voice_combobox.config(values=[])
            self.voice_combobox.config(state="disabled")
            
            self.selected_voice_index = None
        else:
            self.voice_combobox.config(state="normal")
            options = [str(i + 1) for i in range(self.voices_number)]
            self.voice_combobox.config(values=options)
    
    def _sync_instrument_with_voice(self):
        self._is_syncing_ui = True

        memoria = getattr(self, 'user_selected_instruments', {})
        
        if self.selected_voice_index is not None:
            
            if self.selected_voice_index in memoria:
                instrument_value = memoria[self.selected_voice_index]
                self.instrument_number_var.set(str(instrument_value))
                
            else:
                voice = self.actions_controller.trigger_get_current_voice(self.selected_voice_index)
                
                if voice:
                    instrument_value = voice.voice_specs.getInstrument()
                    self.instrument_number_var.set(str(instrument_value))
                else:
                    from src.DataClasses.ProjectConfigs import InitialInstruments
                    default_instrument = InitialInstruments.instruments[self.selected_voice_index % 4]
                    self.instrument_number_var.set(str(default_instrument))
                    
        else:
            self.instrument_number_var.set("")

        self._is_syncing_ui = False

    ##############################################
    # Public methods to interact with the GUI:
    ##############################################

    def run(self):
        self.root.mainloop()