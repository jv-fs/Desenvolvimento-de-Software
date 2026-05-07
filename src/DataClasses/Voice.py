from mido import Message, MidiTrack
from src.Components.Mapping import *

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
    
    def getInitialInstrument(self):
        return self.initial_instrument
    
    def getInitialVolume(self):
        return self.initial_volume
    
    def getInitialTonality(self):
        return self.initial_tonality

    def append_midi_message(self, message: str, control: int, value: int, time: int = 0):
        self.midiTrack.append(Message(message, channel=self.channel, control=control, value=value, time=time))
    
    
    def generate_and_get_track(self) -> MidiTrack:
        i = 0
        while i < len(self.text):
            char = self.text[i]
            rules = Mapping.registry.get(char, Mapping.registry.get('default')) # Tries to get the rules for the character, if not found, gets the default rule
            applied = False
            for rule in rules:
                validation = rule.RuleCheck(self.text, i)
                if validation > 0:
                    rule.RuleApply(self.text, self.midiTrack)
                    i += validation
                    applied = True
                    break # If a rule is applied, break the loop to check the next character
            
            if not applied:
                i += 1 # If no rule is applied, move to the next character to avoid infinite loop (security measure for the default case)

        return self.midiTrack
