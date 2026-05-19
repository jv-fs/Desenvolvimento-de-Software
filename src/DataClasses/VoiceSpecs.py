from src.Utils.MIDITable import Instruments, Notes 
from src.DataClasses.ProjectConfigs import VoiceConstants

class VoiceSpecs():
    def __init__(self, instrument: int, channel: int):
        self.instrument = instrument # The MIDI instrument number (0-127)
        self.voice_identifier = channel # The voice identifier, used to determine the channel and other specs based on the voice index
        self.volume = None # Just showing that this spec exists. The initial volume will be generated based on the voice index
        self.octave = None # Just showing that this spec exists. The initial octave will be generated based on the voice index

        self._generateCorrectVolume()
        self._generateCorrectOctave()
    
    def _generateCorrectVolume(self):
        self.volume = VoiceConstants.MAXIMUM_VOLUME - (self.voice_identifier * VoiceConstants.VOLUME_STEP)
        if self.volume < VoiceConstants.MINIMUM_VOLUME:
            self.volume = VoiceConstants.MINIMUM_VOLUME

    def _generateCorrectOctave(self):
        self.octave = VoiceConstants.BASE_OCTAVE - (self.voice_identifier % 4) # This will generate octaves in a cycle of 4 (6, 5, 4, 3, 6, 5, 4, 3, ...)
    
    def _generateDefaultInstrument(self): # Checar
        self.octave = VoiceConstants.BASE_OCTAVE - (self.voice_identifier % 4)

    def getInstrument(self):
        return self.instrument
    
    def getVolume(self):
        return self.volume
    
    def getOctave(self):
        return self.octave

    def getVoiceIdentifier(self):
        return self.voice_identifier

    def setVolume(self, volume: int):
        self.volume = volume
    
    def setOctave(self, octave: int):
        if octave < VoiceConstants.MINIMUM_OCTAVE:
            octave = VoiceConstants.MINIMUM_OCTAVE
        elif octave > VoiceConstants.MAXIMUM_OCTAVE:
            octave = VoiceConstants.MAXIMUM_OCTAVE
        
        self.octave = octave
    
    def setInstrument(self, instrument: int):
        self.instrument = instrument
    
    def setVoiceIdentifier(self, voice_identifier: int):
        self.voice_identifier = voice_identifier