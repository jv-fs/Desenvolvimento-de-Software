from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from mido import MidiTrack
import mido

from src.DataClasses.VoiceSpecs import VoiceSpecs
from src.DataClasses.ProjectConfigs import MappingConstants, RulesConstants
from src.Utils.MIDITable import Notes


class MusicBPMState:
    current_bpm = MappingConstants.INITIAL_BPM
    
    @classmethod
    def increase_bpm(cls):
        cls.current_bpm = min(MappingConstants.MAXIMUM_BPM, cls.current_bpm + MappingConstants.BPM_STEP) # BPM should not go above MAXIMUM_BPM
    
    @classmethod
    def decrease_bpm(cls):
        cls.current_bpm = max(MappingConstants.MINIMUM_BPM, cls.current_bpm - MappingConstants.BPM_STEP) # BPM should not go below MINIMUM_BPM


@dataclass
class RuleMatch:
    is_match: bool
    consumed_chars: int = 0
    payload: Any = None


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
    def RuleCheck(self, text: str, index: int) -> RuleMatch:
        pass

    @abstractmethod
    def RuleApply(self, payload: Any, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        pass

########################
#        Rules:
########################

# IMPORTANT: the rules below must be in priority order, meaning that if a character has more than one rule, the one with higher priority (lower in the code) will be applied first.
# If a rule is applied, the next rules will not be checked for that character, so the order of the rules is important to ensure the correct behavior of the mapping system.

@Mapping.register('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
class NoteRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> RuleMatch:
        return RuleMatch(is_match=True, consumed_chars=1, payload=text[index])

    def RuleApply(self, payload: Any, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        note = Notes.getNoteFromName(payload, voice_specs.getOctave())

        instrument_msg = mido.Message(
            'program_change',
            channel=voice_specs.getVoiceIdentifier(),
            program=voice_specs.getInstrument()
        )

        note_on = mido.Message('note_on', note=note, velocity=64, time=0, channel=voice_specs.getVoiceIdentifier())
        note_off = mido.Message('note_off', note=note, velocity=64, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())

        midiTrack.append(instrument_msg)
        midiTrack.append(note_on)
        midiTrack.append(note_off)

@Mapping.register('M')
class EFlatRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> RuleMatch:
        if text[index + 1] == 'b':
            return RuleMatch(is_match=True, consumed_chars=2, payload='Mb')
        else:
            return RuleMatch(is_match=False)

    def RuleApply(self, payload: Any, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        note = Notes.getNoteFromName(payload, voice_specs.getOctave())
        note_on = mido.Message('note_on', note=note, velocity=64, time=0, channel=voice_specs.getVoiceIdentifier())

        note_off = mido.Message('note_off', note=note, velocity=64, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())
        midiTrack.append(note_on)
        midiTrack.append(note_off)

@Mapping.register('>', '<')
class BPMControlRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> RuleMatch:
        return RuleMatch(is_match=True, consumed_chars=1, payload=text[index])
    
    def RuleApply(self, payload: Any, midiTrack: MidiTrack, _voice_specs: VoiceSpecs):
        if payload == '>':
            MusicBPMState.increase_bpm()
        else:
            MusicBPMState.decrease_bpm()

        new_tempo = mido.bpm2tempo(MusicBPMState.current_bpm)
        tempo_message = mido.MetaMessage('set_tempo', tempo=new_tempo, time=0)
        midiTrack.append(tempo_message)

@Mapping.register('!', ';', ',')
class InstrumentChangeRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> RuleMatch:
        return RuleMatch(is_match=True, consumed_chars=1, payload=text[index])
    
    def RuleApply(self, payload: Any, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        instrument_value = RulesConstants.intrument_rules_characters.get(payload)
        program_change_message = mido.Message('program_change', program=instrument_value, time=0, channel=voice_specs.getVoiceIdentifier())
        midiTrack.append(program_change_message)
        voice_specs.setInstrument(instrument_value) 

@Mapping.register('V', '?')
class OctaveControlRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> RuleMatch:
        return RuleMatch(is_match=True, consumed_chars=1, payload=text[index])
    
    def RuleApply(self, payload: Any, _midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        # Respects the interval of octaves defined by MINIMUM_OCTAVE and MAXIMUM_OCTAVE 
        # If the new octave goes below the minimum, it should wrap around to the maximum.
        current_octave = voice_specs.getOctave()
        
        if payload == 'V':
            new_octave = current_octave - 1 
        else:
            new_octave = current_octave + 1

        voice_specs.setOctave(new_octave)  # Exceptions for octave limits are handled inside the setOctave method of VoiceSpecs, which will ensure the octave stays within the defined range.

@Mapping.register('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
class LowerCasePauseRule(Mapping):
    def RuleCheck(self, _text: str, _index: int) -> RuleMatch:
        return RuleMatch(is_match=True, consumed_chars=1)

    def RuleApply(self, _payload: Any, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        pause = mido.Message('note_off', note=0, velocity=0, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())
        midiTrack.append(pause)

@Mapping.register('[')
class initialPausesRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> RuleMatch:
        end_index = text.find(']', index)

        if end_index != -1:
            #gets all the content between the brackets
            inner_content = text[index + 1:end_index]

            if inner_content.isdigit():
                pauses = int(inner_content)
                return RuleMatch(is_match=True, consumed_chars=(end_index - index) + 1, payload=pauses)

        return RuleMatch(is_match=False)
    
    def RuleApply(self, payload: Any, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        delay_ticks = payload * MappingConstants.TICKS_PER_BEAT
        pause_message = mido.Message('note_off', note=0, velocity=0, time=delay_ticks, channel=voice_specs.getVoiceIdentifier())
        midiTrack.append(pause_message)

@Mapping.register(is_default=True)
class DefaultRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> RuleMatch:
        previous_char = text[index - 1] if index > 0 else ""
        previous_previous_char = text[index - 2] if index > 1 else ""

        full_note = previous_previous_char + previous_char
        
        if (Notes.getNoteFromName(previous_char, 0) is not None): # The octave is not important here, since we are just checking if the character is a note, so it is a zero for the octave parameter
            return RuleMatch(is_match=True, consumed_chars=1, payload=previous_char)
        elif (Notes.getNoteFromName(full_note, 0) is not None):
            return RuleMatch(is_match=True, consumed_chars=1, payload=full_note)
        else:
            return RuleMatch(is_match=True, consumed_chars=1, payload=None)

    def RuleApply(self, payload: Any, midiTrack: MidiTrack, voice_specs: VoiceSpecs):
        if payload:
            note = Notes.getNoteFromName(payload, voice_specs.getOctave())

            note_on = mido.Message('note_on', note=note, velocity=64, time=0, channel=voice_specs.getVoiceIdentifier())
            note_off = mido.Message('note_off', note=note, velocity=64, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())

            midiTrack.append(note_on)
            midiTrack.append(note_off)
            
        else: # If there is no previous note, we can consider this character as a pause
            pause = mido.Message('note_off', note=0, velocity=0, time=MappingConstants.TICKS_PER_BEAT, channel=voice_specs.getVoiceIdentifier())
            midiTrack.append(pause)