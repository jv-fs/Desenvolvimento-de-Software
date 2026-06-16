class InstrumentController:

    def __init__(self, midi_writer):
        self.midi_writer = midi_writer

    def get_current_voice(self, index):
        return self.midi_writer.get_voice_from_index(index)

    def set_voice_instrument(
        self,
        voice_index,
        instrument
    ):

        voice = self.midi_writer.get_voice_from_index(
            voice_index
        )

        if voice is None:
            return

        if not 0 <= instrument <= 127:
            return

        voice.voice_specs.setInstrument(
            instrument
        )