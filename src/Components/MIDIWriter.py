import tempfile
from pathlib import Path

from src.Components.Voice import Voice
from src.DataClasses.VoiceSpecs import VoiceSpecs
from mido import MidiFile, MidiTrack, Message

class MIDIWriter:
    def __init__(self, mapping, text_operator):
        self.mapping = mapping
        self.text_operator = text_operator
        self.midi_file = MidiFile()
        self.voices = []
        self.temp_midi_path = None

        
    
    def _reset_midi_file(self):
        self.midi_file = MidiFile()
    
    def _reset_voices(self):
        self.voices = []
    
    def _create_voice(self, text: str, instrument: int, voice_index: int):
        voice_specs = VoiceSpecs(instrument, voice_index)
        voice = Voice(text, voice_specs)
        self.voices.append(voice)
    
    def create_voices(self):
        text = self.text_operator.getText()
        if text is not None:
            self._reset_voices()  # Clear existing voices before creating new ones
            for i, line in enumerate(text.splitlines()):
                if line.strip():  # Only create a voice for non-empty lines
                    self._create_voice(line, instrument=1, voice_index=i)
    
    def get_voice_from_index(self, index: int):
        if index is not None and index < len(self.voices):
            return self.voices[index]
        return None
    
    def append_tracks_to_midi_file(self):
        self._reset_midi_file()  # Clear existing tracks before appending new ones
        for voice in self.voices:
            track = voice.generate_and_get_track()
            self.midi_file.tracks.append(track) # CHECAR LIMITAÇÃO DE TRACKS DO MIDI

    def get_midi_file(self):
        return self.midi_file 

    def create_temp_midi_file(self) -> Path:
        temp_file = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
        temp_path = Path(temp_file.name)
        temp_file.close()

        self.midi_file.save(str(temp_path))
        return temp_path
        
    
    def cleanup(self):
        if self.temp_midi_path:
            try:
                self.temp_midi_path.unlink(missing_ok=True)
            except Exception:
                pass

    def __del__(self):
        self.cleanup()