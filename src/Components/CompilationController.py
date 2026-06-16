class CompilationController:

    def __init__(self, midi_writer, midi_player):
        self.midi_writer = midi_writer
        self.midi_player = midi_player

    def prepare_voices(self):
        self.midi_writer.create_voices()

    def finish_compile(self):

        self.midi_writer.append_tracks_to_midi_file()

        temp_midi_path = (
            self.midi_writer.create_temp_midi_file()
        )

        self.midi_player.set_midi_temp(
            temp_midi_path
        )

        self.midi_writer.cleanup()