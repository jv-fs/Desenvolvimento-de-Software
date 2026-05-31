from src.Utils.Exporter import ExportMidiFile

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
    
    def trigger_prepare_voices(self):
        self.midi_writer.create_voices()

    def trigger_finish_compile(self):
        self.midi_writer.append_tracks_to_midi_file()
        temp_midi_path = self.midi_writer.create_temp_midi_file()
        self.midi_player.set_midi_temp(temp_midi_path)
        self.midi_writer.cleanup()

    def trigger_get_is_playing(self):
        return self.midi_player.is_playing()
    
    def trigger_get_is_loop_enabled(self):
        return self.midi_player.is_loop_enabled()
    
    def trigger_save_file(self, destination_path):
        ExportMidiFile.export(destination_path, self.midi_player.temp_midi_path)

    def get_temp_midi_temp(self):
        return self.midi_player.temp_midi_path

    def trigger_set_volume(self, volume: float):
        self.midi_player.set_volume(volume)

    def trigger_set_voice_instrument(self, voice_index: int, instrument: int):
        voice = self.midi_writer.get_voice_from_index(voice_index)
        if voice is not None and 0 <= instrument <= 127:
            voice.voice_specs.setInstrument(instrument)
    
    