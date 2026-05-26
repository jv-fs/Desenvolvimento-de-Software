from mido import Message, MidiTrack
from src.Components.Mapping import *

from src.Utils.MIDITable import Instruments, Notes 
from src.DataClasses.ProjectConfigs import VoiceConstants
from src.DataClasses.VoiceSpecs import VoiceSpecs

class Voice:
    def __init__(self, text: str, voice_specs: VoiceSpecs):
        self.text = text
        self.voice_specs = voice_specs
        self.midiTrack = MidiTrack()

    def setText(self, text: str):
        self.text = text
    
    def getInstrument(self):
        return self.voice_specs.getInstrument()
    
    def getVolume(self):
        return self.voice_specs.getVolume()
    
    def getOctave(self):
        return self.voice_specs.getOctave()
        
    def generate_and_get_track(self) -> MidiTrack:
        i = 0
        while i < len(self.text):
            char = self.text[i]
            rules = Mapping.registry.get(char, Mapping.registry.get('default'))
            applied = False

            for rule in rules:
                match_result = rule.RuleCheck(self.text, i)
                
                if match_result.is_match:
                    rule.RuleApply(match_result.payload, self.midiTrack, self.voice_specs)
                    
                    i += match_result.consumed_chars
                    applied = True
                    break 
            
            if not applied:
                i += 1 

        return self.midiTrack
