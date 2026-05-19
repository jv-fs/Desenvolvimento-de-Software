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
            rules = Mapping.registry.get(char, Mapping.registry.get('default')) # Tries to get the rules for the character, if not found, gets the default rule
            applied = False
            for rule in rules: # Checks the rules for the character, if a rule is valid, applies it and breaks the loop to check the next character
                validation = rule.RuleCheck(self.text, i)
                if validation > 0: # If the rule is valid, applies it and moves the index according to the validation value (some rules may need to jump more than one character)
                    rule.RuleApply(char, self.midiTrack, self.voice_specs)
                    i += validation
                    applied = True
                    break # If a rule is applied, break the loop to check the next character
            
            if not applied:
                i += 1 # If no rule is applied, move to the next character to avoid infinite loop (security measure for the default case)

        return self.midiTrack
