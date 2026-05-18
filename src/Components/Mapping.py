from abc import ABC, abstractmethod
from collections import defaultdict

from mido import Message, MidiTrack, MetaMessage, bpm2tempo
import mido

RULE_VALID_JUMPING_VALUE = 2
RULE_VALID_VALUE = 1
RULE_INVALID_VALUE = 0

TICKS_PER_BEAT = 480 # one beat is 480 ticks.
INITIAL_BPM = 120
MINIMUM_BPM = 10
MAXIMUM_BPM = 300
MINIMUM_OCTAVE = 3
MAXIMUM_OCTAVE = 6

global_music_state = {##TO DO: Dessa forma o bpm segue acumulando para cada compilação e nunca reseta (só se fechar o app).
    'current_bpm': INITIAL_BPM
}

noteDictionary = { # starts by central octave
        'C': 60, # C4
        'D': 62,  # D4
        'Mb': 63, # Eb4
        'E': 64, # E4
        'F': 65, # F4
        'G': 67, # G4
        'A': 69, # A4
        'H': 70, # Bb4
        'B': 71  # B4
    }

instrumentDictionary = {
    '!': 22, # Harmonica
    ';': 15, # Tubular Bells
    ',': 20, # Church Organ
}

class Mapping(ABC):
    registry = defaultdict(list)

    @classmethod
    def register(cls, *chars, is_default=False):
        def wrapper(subclass):
            instance = subclass()
            for char in chars:
                cls.registry[char].append(instance)
            if is_default:
                cls.registry['default'].append(instance)
            return subclass
        return wrapper

    @abstractmethod
    def RuleCheck(self, text: str, index: int) -> int:
        pass

    @abstractmethod
    def RuleApply(self, char: str, voice: 'Voice'):
        pass

########################
#        Rules:
########################

# IMPORTANT: the rules below must be in priority order, meaning that if a character has more than one rule, the one with higher priority (lower in the code) will be applied first.
# If a rule is applied, the next rules will not be checked for that character, so the order of the rules is important to ensure the correct behavior of the mapping system.

@Mapping.register('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
class NoteRule(Mapping):

    def RuleCheck(self, text: str, char_index: int) -> int:
        return RULE_VALID_VALUE

    def RuleApply(self, char: str, voice: 'Voice'): # Colocar um try seria legal talvez?
        note = noteDictionary.get(char)
        note_on = mido.Message('note_on', note=note+voice.getOctaveOffset(), velocity=64, time=0)

        note_off = mido.Message('note_off', note=note+voice.getOctaveOffset(), velocity=64, time=TICKS_PER_BEAT)
        voice.midiTrack.append(note_on)
        voice.midiTrack.append(note_off)

@Mapping.register('M')
class EFlatRule(Mapping):
    def RuleCheck(self, text: str, char_index: int) -> int:
        if text[char_index + 1] == 'b':
            return RULE_VALID_JUMPING_VALUE
        else:
            return RULE_INVALID_VALUE

    def RuleApply(self, char: str, voice: 'Voice'):
        note = noteDictionary.get('Mb')
        note_on = mido.Message('note_on', note=note, velocity=64, time=0)

        note_off = mido.Message('note_off', note=note, velocity=64, time=TICKS_PER_BEAT)
        voice.midiTrack.append(note_on)
        voice.midiTrack.append(note_off)

@Mapping.register('>', '<')
class BPMControlRule(Mapping):

    def RuleCheck(self, text: str, char_index: int) -> int:
        return RULE_VALID_VALUE
    
    def RuleApply(self, char: str, voice: 'Voice'):

        step = 10

        if char == '>':
            global_music_state['current_bpm'] = min(MAXIMUM_BPM, global_music_state['current_bpm'] + step) # BPM should not go above MAXIMUM_BPM
        else:
            global_music_state['current_bpm'] = max(MINIMUM_BPM, global_music_state['current_bpm'] - step) # BPM should not go below MINIMUM_BPM

        print(f"Current BPM: {global_music_state['current_bpm']}")
        new_tempo = mido.bpm2tempo(global_music_state['current_bpm'])
        tempo_message = mido.MetaMessage('set_tempo', tempo=new_tempo, time=0)
        voice.midiTrack.append(tempo_message)

@Mapping.register('!', ';', ',')
class InstrumentChangeRule(Mapping):

    def RuleCheck(self, text: str, char_index: int) -> int:
        return RULE_VALID_VALUE
    
    def RuleApply(self, char: str, voice: 'Voice'):
        instrument_value = instrumentDictionary.get(char)
        program_change_message = mido.Message('program_change', program=instrument_value, time=0)
        voice.midiTrack.append(program_change_message)
        voice.setInitialInstrument(instrument_value) 

@Mapping.register('V', '?')
class OctaveControlRule(Mapping):

    def RuleCheck(self, text: str, char_index: int) -> int:
        return RULE_VALID_VALUE
    
    def RuleApply(self, char: str, voice: 'Voice'):
        # Respects the interval of octaves defined by MINIMUM_OCTAVE and MAXIMUM_OCTAVE 
        # If the new octave goes below the minimum, it should wrap around to the maximum.
        current_octave = voice.getInitialOctave()
        
        if char == 'V':
            new_octave = current_octave - 1 
            if  (new_octave) <  MINIMUM_OCTAVE:
                new_octave = MAXIMUM_OCTAVE 
        else:
            new_octave = current_octave + 1
            if  (new_octave) >  MAXIMUM_OCTAVE:
                new_octave = MINIMUM_OCTAVE
        voice.setInitialOctave(new_octave)  

@Mapping.register('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
class LowerCasePauseRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> int:
        return RULE_VALID_VALUE

    def RuleApply(self, char: str, voice: 'Voice'):
        pause = mido.Message('note_off', note=0, velocity=0, time=TICKS_PER_BEAT)
        voice.midiTrack.append(pause)

@Mapping.register('[')
class initialPausesRule(Mapping):
    pauses = 0
    def RuleCheck(self, text: str, index: int) -> int:
        end_index = text.find(']', index)

        if end_index != -1:
            #gets all the content between the brackets
            inner_content = text[index + 1:end_index]

            if inner_content.isdigit():
                self.pauses = int(inner_content)
                return (end_index - index) + 1 # returns the length of the whole content to jump it in the main loop

        return RULE_INVALID_VALUE
    
    def RuleApply(self, char: str, voice: 'Voice'):
        delay_ticks = self.pauses * TICKS_PER_BEAT
        pause_message = mido.Message('note_off', note=0, velocity=0, time=delay_ticks)
        voice.midiTrack.append(pause_message)

@Mapping.register(is_default=True)
class DefaultRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> int:
        return 1

    def RuleApply(self, char: str, midiTrack: MidiTrack):
        pass # Regra padrão para caracteres sem mapeamento específico