import tkinter as tk
from tkinter import filedialog

ERROR_DISPLAY_DURATION = 3000


class ActionsController:
    def __init__(self, midi_player, text_operator, midi_writer):
        self.midi_player = midi_player
        self.text_operator = text_operator
        self.midi_writer = midi_writer

    def trigger_play(self):
        self.midi_player.play()
    
    def trigger_stop(self):
        self.midi_player.stop()

    def trigger_restart(self):
        self.midi_player.restart()
    
    def trigger_loop(self):
        self.midi_player.toggle_loop()

    def trigger_load_data(self, path):
        self.text_operator.load_data(path)

    def trigger_get_text(self):
        return self.text_operator.getText()
    
    def trigger_has_error(self):
        return self.text_operator.has_error()
    
    def trigger_get_current_voice(self, index):
        return self.midi_writer.get_voice_from_index(index)
    
    def trigger_set_text(self, text):
        self.text_operator.setText(text)
    
    def trigger_compile(self):
        self.midi_writer.create_voices()
        self.midi_writer.append_tracks_to_midi_file()
        temp_midi_path = self.midi_writer.create_temp_midi_file()
        self.midi_player.set_midi_temp(temp_midi_path)

        self.midi_writer.cleanup()

    def trigger_get_is_playing(self):
        return self.midi_player.is_playing()
    
    def trigger_get_is_loop_enabled(self):
        return self.midi_player.is_loop_enabled()