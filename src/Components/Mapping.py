from abc import ABC, abstractmethod
from collections import defaultdict

from mido import Message, MidiTrack, MetaMessage, bpm2tempo
import mido

from src.DataClasses.VoiceSpecs import VoiceSpecs
from src.DataClasses.ProjectConfigs import MappingConstants, InitialInstruments, RulesConstants, VoiceConstants
from src.DataClasses.MIDITable import Instruments, Notes


class MusicState:
    current_bpm = MappingConstants.INITIAL_BPM

    @classmethod
    def reset(cls):
        cls.current_bpm = MappingConstants.INITIAL_BPM
    
    @classmethod
    def increase_bpm(cls):
        cls.current_bpm = min(MappingConstants.MAXIMUM_BPM, cls.current_bpm + MappingConstants.BPM_STEP) # BPM should not go above MAXIMUM_BPM
    
    @classmethod
    def decrease_bpm(cls):
        cls.current_bpm = max(MappingConstants.MINIMUM_BPM, cls.current_bpm - MappingConstants.BPM_STEP) # BPM should not go below MINIMUM_BPM
    
    @classmethod
    def get_current_bpm(cls):
        return cls.current_bpm

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
    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        pass

########################
#        Rules:
########################

# IMPORTANT: the rules below must be in priority order, meaning that if a character has more than one rule, the one with higher priority (lower in the code) will be applied first.
# If a rule is applied, the next rules will not be checked for that character, so the order of the rules is important to ensure the correct behavior of the mapping system.

@Mapping.register('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
class NoteRule(Mapping):
    def RuleCheck(self, text: str, char_index: int) -> int:
        return MappingConstants.RULE_VALID_VALUE

    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs): # Colocar um try seria legal talvez?
        note = Notes.getNoteFromName(char, voice_specs.getOctave())

        note_on = mido.Message('note_on', note=note, velocity=64, time=0, channel=voice_specs.getVoiceIdentifier())
        note_off = mido.Message('note_off', note=note, velocity=64, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())

        midiTrack.append(note_on)
        midiTrack.append(note_off)

@Mapping.register('M')
class EFlatRule(Mapping):
    def RuleCheck(self, text: str, char_index: int) -> int:
        if text[char_index + 1] == 'b':
            return MappingConstants.RULE_VALID_JUMPING_VALUE
        else:
            return MappingConstants.RULE_INVALID_VALUE

    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        note = Notes.getNoteFromName('Mb', voice_specs.getOctave())
        note_on = mido.Message('note_on', note=note, velocity=64, time=0, channel=voice_specs.getVoiceIdentifier())

        note_off = mido.Message('note_off', note=note, velocity=64, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())
        midiTrack.append(note_on)
        midiTrack.append(note_off)

@Mapping.register('>', '<')
class BPMControlRule(Mapping):
    def RuleCheck(self, text: str, char_index: int) -> int:
        return MappingConstants.RULE_VALID_VALUE
    
    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs):

        if char == '>':
            MusicState.increase_bpm()
        else:
            MusicState.decrease_bpm()

        new_tempo = mido.bpm2tempo(MusicState.current_bpm)
        tempo_message = mido.MetaMessage('set_tempo', tempo=new_tempo, time=0)
        midiTrack.append(tempo_message)

@Mapping.register('!', ';', ',')
class InstrumentChangeRule(Mapping):
    def RuleCheck(self, text: str, char_index: int) -> int:
        return MappingConstants.RULE_VALID_VALUE
    
    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        instrument_value = RulesConstants.intrument_rules_characters.get(char)
        program_change_message = mido.Message('program_change', program=instrument_value, time=0, channel=voice_specs.getVoiceIdentifier())
        midiTrack.append(program_change_message)
        voice_specs.setInstrument(instrument_value) 

@Mapping.register('V', '?')
class OctaveControlRule(Mapping):
    def RuleCheck(self, text: str, char_index: int) -> int:
        return MappingConstants.RULE_VALID_VALUE
    
    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        # Respects the interval of octaves defined by MINIMUM_OCTAVE and MAXIMUM_OCTAVE 
        # If the new octave goes below the minimum, it should wrap around to the maximum.
        current_octave = voice_specs.getOctave()
        
        if char == 'V':
            new_octave = current_octave - 1 
        else:
            new_octave = current_octave + 1

        voice_specs.setOctave(new_octave)  # Exceptions for octave limits are handled inside the setOctave method of VoiceSpecs, which will ensure the octave stays within the defined range.

@Mapping.register('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
class LowerCasePauseRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> int:
        return MappingConstants.RULE_VALID_VALUE

    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        pause = mido.Message('note_off', note=0, velocity=0, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())
        midiTrack.append(pause)

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

        return MappingConstants.RULE_INVALID_VALUE
    
    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        delay_ticks = self.pauses * MappingConstants.TICKS_PER_BEAT
        pause_message = mido.Message('note_off', note=0, velocity=0, time=delay_ticks, channel=voice_specs.getVoiceIdentifier())
        midiTrack.append(pause_message)

@Mapping.register(is_default=True)
class DefaultRule(Mapping):
    previous_note = None
    def RuleCheck(self, text: str, char_index: int) -> int:
        previous_char = text[char_index - 1] if char_index > 0 else ""
        previous_previous_char = text[char_index - 2] if char_index > 1 else ""

        full_note = previous_previous_char + previous_char
        
        if (Notes.getNoteFromName(previous_char, 0) is not None): # The octave is not important here, since we are just checking if the character is a note, so it is a zero for the octave parameter
            self.previous_note = previous_char
        elif (Notes.getNoteFromName(full_note, 0) is not None):
            self.previous_note = full_note
        else:
            self.previous_note = None

        return MappingConstants.RULE_VALID_VALUE

    def RuleApply(self, char: str, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        if self.previous_note:
            note = Notes.getNoteFromName(self.previous_note, voice_specs.getOctave())

            note_on = mido.Message('note_on', note=note, velocity=64, time=0, channel=voice_specs.getVoiceIdentifier())
            note_off = mido.Message('note_off', note=note, velocity=64, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())

            midiTrack.append(note_on)
            midiTrack.append(note_off)
            
        else: # If there is no previous note, we can consider this character as a pause
            pause = mido.Message('note_off', note=0, velocity=0, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())
            midiTrack.append(pause)
