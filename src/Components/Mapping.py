from abc import ABC, abstractmethod
from collections import defaultdict

from mido import Message, MidiTrack
import mido

RULE_VALID_JUMPING_VALUE = 2
RULE_VALID_VALUE = 1
RULE_INVALID_VALUE = 0

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
    def RuleCheck(text: str, index: int) -> int:
        pass

    @abstractmethod
    def RuleApply(self,char: str, midiTrack: MidiTrack):
        pass

########################
#        Rules:
########################

# IMPORTANT: the rules below must be in priority order, meaning that if a character has more than one rule, the one with higher priority (lower in the code) will be applied first.
# If a rule is applied, the next rules will not be checked for that character, so the order of the rules is important to ensure the correct behavior of the mapping system.

@Mapping.register('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
class NoteRule(Mapping):
    dictionary = {
        'A': 60, # C4
        'B': 62, # D4
        'C': 64, # E4
        'D': 65, # F4
        'E': 67, # G4
        'F': 69, # A4
        'G': 71, # B4
        'H': 72  # C5
    }

    def RuleCheck(self, text: str, index: int) -> int:
        return RULE_VALID_VALUE

    def RuleApply(self,char: str, midiTrack: MidiTrack): # Colocar um try seria legal talvez?
        note = self.dictionary.get(char)
        note_on = mido.Message('note_on', note=note, velocity=64, time=0)

        note_off = mido.Message('note_off', note=note, velocity=64, time=480)
        midiTrack.append(note_on)
        midiTrack.append(note_off)

@Mapping.register('M')
class EFlatRule(Mapping):
    def RuleCheck(self, text: str, next_index: int) -> int:
        if text[next_index] == 'b':
            return RULE_VALID_JUMPING_VALUE
        else:
            return RULE_VALID_VALUE

    def RuleApply(self, text: str, index: int):
        pass # Associa Mi bemol ao devido lugar

@Mapping.register(is_default=True)
class DefaultRule(Mapping):
    def RuleCheck(self, text: str, index: int) -> int:
        return 1

    def RuleApply(self, text: str, index: int):
        pass # Regra padrão para caracteres sem mapeamento específico