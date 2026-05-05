from mido import Message, MidiTrack

class Voice:
    def __init__(self, text: str, instrument: int, volume: int, tonality: str):
        self.text = text
        self.initial_instrument = instrument
        self.initial_volume = volume
        self.initial_tonality = tonality
        self.channel = 0  # Default MIDI channel, can be set later
        self.midiTrack = MidiTrack()

    def setText(self, text: str):
        self.text = text

    def setChannel(self, channel: int):
        self.channel = channel

    def setInitialInstrument(self, instrument: int):
        self.initial_instrument = instrument

    def setInitialVolume(self, volume: int):
        self.initial_volume = volume

    def setInitialTonality(self, tonality: str):
        self.initial_tonality = tonality
    
    def getMidiTrack(self):
        return self.midiTrack
    
    def getInitialInstrument(self):
        return self.initial_instrument
    
    def getInitialVolume(self):
        return self.initial_volume
    
    def getInitialTonality(self):
        return self.initial_tonality

    def append_midi_message(self, message: str, control: int, value: int, time: int = 0):
        self.midiTrack.append(Message(message, channel=self.channel, control=control, value=value, time=time))