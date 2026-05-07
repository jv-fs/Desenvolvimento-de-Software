from src.DataClasses.Voice import Voice
from mido import MidiFile, MidiTrack, Message

class MIDIWriter:
    def __init__(self, mapping, text_operator):
        self.mapping = mapping
        self.text_operator = text_operator
        self.midi_file = MidiFile()
        self.voices = []
    
    def _reset_midi_file(self):
        self.midi_file = MidiFile()
    
    def _reset_voices(self):
        self.voices = []
    
    def _create_voice(self, text: str, instrument: int, volume: int, tonality: str):
        voice = Voice(text, instrument, volume, tonality)
        self.voices.append(voice)
    
    def create_voices(self):
        text = self.text_operator.getText()
        if text is not None:
            self._reset_voices()  # Clear existing voices before creating new ones
            for line in text.splitlines():
                if line.strip():  # Only create a voice for non-empty lines
                    self._create_voice(line, instrument=1, volume=100, tonality="C") # Example values, customize this based on mapping logic
    
    def get_voice_from_index(self, index: int):
        if index is not None and index < len(self.voices):
            return self.voices[index]
        return None
    
    def append_tracks_to_midi_file(self):
        self._reset_midi_file()  # Clear existing tracks before appending new ones
        for voice in self.voices:
            track = voice.generate_and_get_track()
            self.midi_file.tracks.append(track) # Verify if this dont extrapolate the midi file limit of 16 tracks (if it does, we need to merge tracks)